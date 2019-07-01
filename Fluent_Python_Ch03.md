<!-- MarkdownTOC -->

- 第四章 字典与集合
    - 字典概览
        - 构建字典的两类方法：
        - `dict`、`defaultdict`和`OrderedDict`常见方法
        - `d.get(k, default)`与`d.setdefault(k, default)`比较

<!-- /MarkdownTOC -->

### 第四章 字典与集合

#### 字典概览
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
但是后者至少要进行两次键查询——如果键不存在的话就是三次查询，用`setdefault`只需要一次就可以完成整个惭怍。
