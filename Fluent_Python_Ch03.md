<!-- MarkdownTOC -->

- 第四章 字典与集合
    - 字典概览
        - 构建字典的两类方法：
        - `dict`、`defaultdict`和`OrderedDict`常见方法
        - `d.get(k, default)`与`d.setdefault(k, default)`比较
        - 处理找不到键的两种选择
            - 使用`defaultset`
            - 使用特殊方法`__missing__`
        - 子类化UserDict
        - 不可变映射类型MappingProxyType

<!-- /MarkdownTOC -->

### 第四章 字典与集合

#### 字典
##### 构建字典的两类方法：

- 一是字典的构造方法
```python
>>> a = dict(one=1, two=2, three=3)
>>> b = {'one':1, 'two':2, 'three':3}
>>> c= dict(zip(['one', 'two', 'three'], [1, 2, 3]))
>>> d = dict([('two', 2), ('one', 1), ('three', 3)])
>>> e = dict({'three':3, 'two':2, 'one':1})
>>> a == b == c == d == e
True
```

- 二是字典推导(dictcomp)
示例3-1利用字典推导把一个装满元组的列表变成两个不同的字典
```python
>>> DIAL_CODES = [
... (86, 'China'),
... (91, 'India'),
... (1, 'United States'),
... (62, 'Indonesia'),
... (55, 'Brazil'),
... (92, 'Pakistan'),
... (880, 'Bangladesh'),
... (234, 'Nigeria'),
... (7, 'Russia'),
... (81, 'Japan'),
... ]
>>> country_code = {country: code for code, country in DIAL_CODES}
>>> country_code
{'China': 86, 'India': 91, 'United States': 1, 'Indonesia': 62, 'Brazil': 55, 'Pakistan': 92, 'Bangladesh': 880, 'Nigeria': 234, 'Russia': 7, 'Japan': 81}
>>> {code: country.upper() for country, code in country_code.items() if code < 66}
{1: 'UNITED STATES', 62: 'INDONESIA', 55: 'BRAZIL', 7: 'RUSSIA'}
```

##### `dict`、`defaultdict`和`OrderedDict`常见方法

略

##### `d.get(k, default)`与`d.setdefault(k, default)`比较
前置知识：

1. `re.compile()`函数根据一个模式字符串和可选的标志参数生成一个正则表达式对象。该对象拥有一系列方法用于正则表达式匹配和替换。 
2. 获取文件对象之后可以通过迭代器来访问：`for line in f: print line `。
3. `re.finditer()`函数在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回。
```python
import re
 
it = re.finditer(r"\d+","12a32bc43jf3") 
for match in it: 
    print (match.group() )

# 输出
12 
32 
43 
3
```
4. `group()`返回被 RE 匹配的字符串。
5. `start()`返回匹配开始的位置
   

示例3-2 index0.py 这段程序从索引中获取单词出现的频率信
息，并把它们写进对应的列表里。
```python
"""创建一个从单词到其出现情况的映射"""

import sys
import re

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            occurences = index.get(word, [])
            occurences.append(location)
            index[word] = occurences

# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
```

示例3-3 index.py 用一行就解决了获取和更新单词的出现情况列
表，当然跟示例3-2不一样的是，这里用到了`dict.setdefault`
```python
"""创建一个从单词到其出现情况的映射"""

import sys
import re

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefualt(word, []).append(location)

# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
```
`index.setdefualt(word, []).append(location)`等价于
```python
if key not in my_dict:
    my_dict[key] = []
my_dict[key].append(new_value)
```
但是后者至少要进行两次键查询——如果键不存在的话就是三次查询，用`setdefault`只需要一次就可以完成整个操作。

##### 处理找不到键的两种选择
###### 使用`defaultset`
前置知识：

在实例化一个`defaultdict`的时候，需要给构造方法提供
一个可调用对象，这个可调用对象会在`__getitem__`碰到找不到的键
的时候被调用，让`__getitem__`返回某种默认值。例如新建一个字典：`dd = defaultdict(list)`，如果键
'new-key'在dd中还不存在的话：

- 调用list()来新建一个列表
- 把这个新列表作为值，'new_key'作为键，放到dd中
- 返回这个列表的引用

示例3-4：
``` python
"""创建一个从单词到其出现情况的映射"""

import sys
import re
import collections

WORD_RE = re.compile(r'\w+')

index = collections.defaultdict(list)
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)

# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
```
**注意**：`defaultdict`的默认值只会在`__getitem__`方法中被调用，即`dd[k]`这个表达
式会调用`default_factory`创造某个默认值，而`dd.get(k)`则会
返回 None。

###### 使用特殊方法`__missing__`
示例3-5：
```python
class StrKeyDict(dict):
    """docstring for StrKeyDict"""
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()

if __name__ == '__main__':
    
    d = StrKeyDict([('2', 'two'), ('4', 'four')])

    print(d.get('2'))
    print(d.get(4))
    print(d.get(1))

    print(2 in d)
    print(1 in d)

    print(d['2'])
    print(d[4])
    print(d[1])

# 输出
# Tests for item retrieval using `d.get(key)` notation::
two
four
None

# Tests for the `in` operator::
True
False

# Tests for item retrieval using `d[key]` notation::
two
four
Traceback (most recent call last):
  File "StrKeyDict0.py", line 30, in <module>
    print(d[1])
  File "StrKeyDict0.py", line 6, in __missing__
    return self[str(key)]
  File "StrKeyDict0.py", line 5, in __missing__
    raise KeyError(key)
KeyError: '1'
```
下面来看看为什么`isinstance(key, str)`测试在上面的`__missing__`中是必需的。  
如果没有这个测试，只要 str(k) 返回的是一个存在的键，那么`__missing__` 方法是没问题的，不管是字符串键还是非字符串键，它都能正常运行。但是如果 str(k) 不是一个存在的键，代码就会陷入无限递归。这是因为`__missing__`的最后一行中的`self[str(key)]`会调用`__getitem__`，而这个`str(key)`又不存在，于是`__missing__`又会被调用。

为了保持一致性`__contains__`方法在这里也是必需的。这是因为`k in d`这个操作会调用它，但是我们从`dict`继承到的`__contains__`方法不会在找不到键的时候调用`__missing__`方法。`__contains__`里还有个细节，就是我们这里没有用更具Python风格的方式——`k in my_dict`——来检查键是否存在，因为那也会导致`__contains__`被递归调用。为了避免这一情况，这里采取了更显式的方法，直接在这个`self.keys()`里查询。

**注意**：

1. 同`defaultdict`一样，`__missing__`方法只会被`__getitem__`调用，对`get`或者`__contains__`(in运算符会用到这个方法)这些方法的使用没有影响。
2. 如果要自定义一个映射类型，更合适的策略其实是继承
`collections.UserDict`类

##### 子类化UserDict
*暂时还不太理解为什么要使用UserDict类*

示例3-6：无论是添加、更新还是查询操作，StrKeyDict 都会把非字符串的键转换为字符串
```python
import collections

class StrDictKey(collections.UserDict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item
```

##### 不可变映射类型MappingProxyType
标准库里所有的映射类型都是可变的，但有时候你会有这样的需求，比如不能让用户错误地修改某个映射。我们可以使用types模块中的MappingProxyType类，如果给这个类一个映射，它会返回一个**动态的**、**只读的**映射类型。也就说，着如果对原映射做出了改动，我们通过这个视图可以观察到，但是无法通过这个视图对原映射做出修改。

示例3-6：
```python
>>> from types import MappingProxyType
>>> d = {1:'A'}
>>> d_proxy = MappingProxyType(d)
>>> d_proxy
mappingproxy({1: 'A'})
>>> d_proxy[1]
'A'
>>> d_proxy[2] = x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'x' is not defined
>>> d[2] = 'B'
>>> d_proxy[2]
'B'
```

#### 集合

##### 集合的字面量

```python
>>> s = {1}
>>> type(s)
<class 'set'>
>>> s
{1}
>>> s.pop()
1 >>> s
set()
```

**注意：如果要创建一个空集，必须用不带任何参数的构造方法 set()。如果只是写成 {} 的形式，跟以前一样，创建的其实是个空字典。**

##### 集合推导式

前置知识：

`unicodedata.name`用以获取字符的名字

```python
>>> from unicodedata import name 
>>> {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i),'')} 
{'§', '=', '¢', '#', '¤', '<', '¥', 'μ', '×', '$', '¶', '£', '©','°', '+', '÷', '±', '>', '¬', '®', '%'}
```

##### 集合的操作

*待填坑*

##### 字典与集合的背后

*待填坑*

