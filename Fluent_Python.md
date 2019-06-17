<!-- MarkdownTOC -->

- 第一章 Python数据模型
- 第二章 序列构成的数组
    - 列表推导和生成器表达式
    - 元组不仅仅是不可变的列表
        - 元组的第一个作用：数据记录
        - 用*来处理剩下的元素
        - 具名元组
        - 元组的第二个作用：作为不可变的列表
    - 切片
    - 对序列使用+和*
        - 建立由列表组成的列表

<!-- /MarkdownTOC -->

#### 第一章 Python数据模型
这一章中，作者介绍了Python数据模型，主要是Python的一些特殊方法，在这里我体会到了“鸭子类型”的含义，只要你在自定义的类中实现了某些特殊方法，例如：`__len__` `__getitem__` `__iter__`等等，你就可以调用`len()` `Object[index]` `for...in...`等函数。

前置知识：  
1. [`Collections.namedtuple()`](#namedtuple):用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。这样一来，我们用namedtuple可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便。
2. `_card`:设置私有变量。
3. `Card._card.index(value)`: 返回列表中`value`对应的索引。
4. `sorted()`函数`key`参数：接受一个函数名，这个函数规定了元素以何种方式进行排序，并返回一个数值。 
5. [列表生成式](#listcomps)

示例1-1展现如何实现`__getitem__`和`__len__`两个特殊方法：
``` python
from collections import namedtuple
from random import choice

Card = namedtuple('Card', ['rank', 'suits'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

deck = FrenchDeck()
# print(len(deck))
# print(deck[0])
# print(deck[-1])
# print(choice(deck))
# print(choice(deck))

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
print(suit_values)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suits]

for card in sorted(deck, key=spades_high):
    print(card)
```

通常，代码无需直接使用特殊方法，除非有大量的元编程存在，直接调用特殊方法的频率应该远远低于你去实现它们的次数。唯一的例外可能是`__init__`方法。
**示例1-2： 创建了一个简单的二维向量类，实现了 `repr()` `abs()` `bool()` `add()` `mul()`方法**
``` python
# Demo1-2.py 一个简单地二维向量类
from math import hypot

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%s, %s)' % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

vec = Vector(2, 5)
print(vec)
```

1. `__repr__`特殊方法可以得到一个对象地字符串表示形式，如果没有实现`__repr__`，当我们在控制台打印一个向量的实例时，得到的字符串可能会是`Vector object at Ox.....`。
2. `repr`和`str`的区别：
    ``` python
    >>> import datetime
    >>> d = datetime.date.today()
    >>> str(d)
    '2011-05-14'
    >>> repr(d)
    'datetime.date(2011, 5, 14)'
    ```

#### 第二章 序列构成的数组
Python序列类型可以分为*容器序列*和*扁平序列*：

- 容器序列：`list` `tuple` `collections.deque`这些序列能存放不同类型的数据，并且存放的是他们所包含的任意类型的对象的引用。
- 扁平序列：`str` `bytes` `bytearray` `memoryview` `array.array` 这些序列只能容纳一种类型，并且存放的值而不是引用，只能存放诸如字符、字节和数值这种基础类型。

>[有关Python对象和引用的理解](https://www.cnblogs.com/ShaunChen/p/5656971.html)

还可以分为*可变序列*和*不可变序列*：

- 可变序列：`list` `bytearray` `array.array` `collections.deque` `memoryview`
- 不可变序列：`tuple` `str` `bytes`

![可变序列与不可变序列](http://ww1.sinaimg.cn/large/6e4e7200ly1g41nqo3u3sj20fi051t9l.jpg)

##### <a id="listcomps">列表推导和生成器表达式 </a>

**示例2-1：列表推导可以帮助我们把一个序列或是其他可迭代类型中的元素过滤或是加工，然后在新建一个列表。**

``` python
# 不使用列表推导式
def str2unicode():
    symbols = '$¢£¥€¤'
    codes = []
    for symbol in symbols:
        codes.append(ord(symbol))

    print(codes)

# 使用列表推导式
def str_to_unicode():
    symbols = '$¢£¥€¤'
    codes = [ord(symbol) for symbol in symbols]
    print(codes)

str2unicode()
str_to_unicode()
```

**示例2-2：列表推导同filter和map的比较**

前置知识：

1. `map()`函数接收两个参数，一个是函数，一个是Iterable，`map`将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
2. 和`map()`类似，`filter()`也接收一个函数和一个序列。和`map()`不同的是，`filter()`把传入的函数依次作用于每个元素，然后根据返回值是`True`还是`False`决定保留还是丢弃该元素。

``` python
>>> symbols = '¢£¥€¤'
>>> beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
>>> beyond_ascii
[162, 163, 165, 8364, 164]
>>> beyond_ascii = list(filter(lambda c : c > 127, map(ord, symbols)))
>>> beyond_ascii
[162, 163, 165, 8364, 164]
```

**示例2-3：笛卡儿积：两个或以上的列表中的元素构成元组，这些元组构成的列表就是笛卡儿积**
```python
>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
# 这个语句得到的结果是先以颜色排列，再以尺码排列
>>> tshirts = [(color, size) for color in colors for size in sizes]
>>> tshirts
[('black', 'S'), ('black', 'M'), ('black', 'L'), ('white', 'S'), ('white', 'M'), ('white', 'L')]
# 双重循环模拟上面的列表推导式
>>> for color in colors:
...     for size in sizes:
...         print((color, size))
... 
('black', 'S')
('black', 'M')
('black', 'L')
('white', 'S')
('white', 'M')
('white', 'L')
# 这个语句得到的结果是先以尺码排列，再以颜色排列
>>> tshirts = [(color, size) for size in sizes for color in colors]
>>> tshirts
[('black', 'S'), ('white', 'S'), ('black', 'M'), ('white', 'M'), ('black', 'L'), ('white', 'L')]
```
列表推导的作用只有一个：**生成列表**。如果想生成其他类型的序列，生成器表达式就派上用场了。

**示例2-4：用生成器表达式初始化元组和数组**

前置知识：

[数组的详细讨论见后](# array)

```python
>>> symbols = '¢£¥€¤'
>>> tuple(ord(symbol) for symbol in symbols)
(162, 163, 165, 8364, 164)
>>> import array
>>> array.array('i', (ord(symbol) for symbol in symbols))
array('i', [162, 163, 165, 8364, 164])
```

**示例2-5：使用生成器表达式计算笛卡儿积**
```python
>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
>>> for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
...     print(tshirt)
... 
black S
black M
black L
white S
white M
white L
```
生成器表达式逐个产出元素，从来不会一次性产出一个含有6个T恤样式的列表。

##### 元组不仅仅是不可变的列表  
###### 元组的第一个作用：数据记录  
元组其实是对数据的记录：元组中的每个元素都存放了记录中一个字段的数据，外加这个字段的位置。正式这个位置信息 给数据赋予了意义。(*对于这句话还有待进一步的理解*)

**示例2-6：把元组用作记录。如果在任何的表达式中我们在元组内对元素排序，这些元素所携带的信息就会丢失，因为这些信息是跟它们的位置有关的。**
```python
>>> traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
>>> for passport in sorted(traveler_ids):
...     print('%s/%s' % passport)
... 
BRA/CE342567
ESP/XDA205856
USA/31195855
>>> for country, _ in traveler_ids:
...     print(country)
... 
USA
BRA
ESP
```
`for`循环可以分别提取元组里的元素，也叫做拆包(unpacking)。因为元组中第二个元素没有什么作用，所以他赋值给`_`占位符。

元组拆包的几种用法：

1. 平行赋值
```python
>>> lax_coordinates = (33.9425, -118.408056)
>>> latitude, longtitude = lax_coordinates # 元组拆包
>>> latitude
33.9425
>>> longtitude
-118.408056
```

2. 交换两个变量的值
```python
>>> b, a = a, b
```

3. 用*号运算符把一个可迭代对象拆开作为函数的参数
前置知识：python divmod() 函数把除数和余数运算结果结合起来，返回一个包含商和余数的元组(a // b, a % b)。
```python
>>> divmod(20, 8)
(2, 4)
>>> t = (20, 8)
>>> divmod(*t)
(2, 4)
>>> quotient, remainder = divmod(*t)
>>> quotient, remainder
(2, 4)
```
除此之外，在元组拆包中使用*也可以帮助我们把注意力集中在元组的部分元素上。  
###### 用*来处理剩下的元素  
在Python中，函数用`*args`来获取不确定数量的参数算是一种经典写法了。这个概念被扩展到了平行赋值中：
```python
>>> a, b, *rest = range(5)
>>> a, b, rest
(0, 1, [2, 3, 4])
>>> a, b, *rest = range(3)
>>> a, b, rest
(0, 1, [2])
>>> a, b, *rest = range(2)
>>> a, b, rest
(0, 1, [])

# 可以出现在赋值表达式的任意位置
>>> a, *body, c, d = range(5)
>>> a, body, c, d
(0, [1, 2], 3, 4)
>>> *head, b, c, d = range(5)
>>> head, b, c, d
([0, 1], 2, 3, 4)
```

4. 函数以元组的形式返回多个值
前置知识：os.path.split()函数会返回以路径和最后一个文件名组成的元组(path, last_part)。
```python
>>> import os
>>> _, filename = os.path.split('F:\\Python code\\Fluent Python\\demo1-2.py')
>>> filename
'demo1-2.py'
```
###### <a id="namedtuple">具名元组</a>
具名元组可以让我们给记录中的字段命名。`collections.namedtuple`是一个工厂函数，他可以用来构建一个带字段名的元组和一个有名字的类。

**示例2-7：用具名元组记录城市的信息**
```python
from collections import namedtuple

City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))

print(tokyo)
print(tokyo.population)
print(tokyo.coordinates)
print(tokyo[1])

# 输出
City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))
36.933
(35.689722, 139.691667)
JP
```
- 创建一个具名元组需要两个参数，一个是类名，另一个是类的各个字段的名字。后者可以是由数个字符串组成的可迭代对象，或者是由空格分隔开的字段名组成的字符串。
- 可以通过`实例.字段名`或`实例.位置`来获取一个字段的信息。

**示例2-8：具名元组的特殊属性**
```python
print(City._fields)
LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)
delhi._asdict()

for key, value in delhi._asdict().items():
    print(key + ':', value)

# 输出
('name', 'country', 'population', 'coordinates')
OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population', 21.935), ('coordinates', LatLong(lat=28.613889, long=77.208889))])
name: Delhi NCR
country: IN
population: 21.935
coordinates: LatLong(lat=28.613889, long=77.208889)
```
- `_fields`属性是一个包含这个类所有字段名称的元组。
- `_make` = `City(*delhi_data)`，接受一个可迭代对象来生成这个类的一个实例。
- `_asdict()`把具名元组以collections.OrderedDict的形式返回。
>注：使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。如果要保持Key的顺序，可以用`OrderedDict`
- 在`delhi`这个实例中，`coordinates`的值也是一个namedtuple

###### 元组的第二个作用：作为不可变的列表  
详见书本。  

##### 切片
**示例2-9：对对象进行切片，下例中纯文本文件形式的收据以一行字符串的形式被解析。**  
前置知识：  
1. `slice() `函数实现切片对象，主要用在切片操作函数里的参数传递。所有使用切片的地方都可以使用切片对象。
```python
>>> items = [0, 1, 2, 3, 4, 5, 6]
>>> a = slice(2, 4)
>>> items[2:4]
[2, 3]
>>> items[a]
[2, 3]
>>> items[a] = [10,11]
>>> items
[0, 1, 10, 11, 4, 5, 6]
>>> del items[a]
>>> items
[0, 1, 4, 5, 6]
```
假定你要从一个记录（比如文件或其他类似格式）中的某些固定位置提取字段：
```python
>>>record = '....................100 .......513.25 ..........'
>>>cost = int(record[20:23]) * float(record[31:37])
```
与其这样写，可以直接命名切片：
```python
>>>SHARES = slice(20, 23)
>>>PRICE = slice(31, 37)
>>>cost = int(record[SHARES]) * float(record[PRICE])
```
此时，再来看书中的例子就比较清楚了：
```python
>>> invoice = """
... 0.....6................................40........52...55........
... 1909  Pimoroni PiBrella                    $17.50    3    $52.50
... 1489  6mm Tactile Switch x20                $4.95    2    $9.90
... 1510  Panavise Jr. - PV-201                $28.00    1    $28.00
... 1601  PiTFT Mini Kit 320x240               $34.95    1    $34.95
... """
>>> SKU = slice(0, 6)
>>> DESCRIPTION = slice(6, 40)
>>> UNIT_PRICE = slice(40, 52)
>>> QUANTITY = slice(52, 55)
>>> ITEM_TOTAL = slice(55, None)
>>> line_items = invoice.split('\n')[2:]
>>> for item in line_items:
...     print(item[UNIT_PRICE], item[DESCRIPTION])
... 
   $17.50    Pimoroni PiBrella                 
    $4.95    6mm Tactile Switch x20            
   $28.00    Panavise Jr. - PV-201             
   $34.95    PiTFT Mini Kit 320x240
```

如果把切片放在赋值语句的左边，或把它作为del操作的对象，我们就可以对序列进行嫁接、切除和就地修改操作。
```python
>>> l = list(range(1, 10))
>>> l
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> l[2:5] = [20, 30]
>>> l
[1, 2, 20, 30, 6, 7, 8, 9]
>>> del l[5:7]
>>> l
[1, 2, 20, 30, 6, 9]
>>> l[3::2] = [11, 22]
>>> l
[1, 2, 20, 11, 6, 22]
>>> l[2:5] = 100
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only assign an iterable
>>> l[2:5] = [100]
>>> l
[1, 2, 100, 22]
```
**注意**：切片赋值操作的等式右边必须是可迭代对象。

##### 对序列使用+和*
对序列使用*和+操作符时，不会修改原有的对象，而是会新建一个包含同样类型数据的序列来作为结果。
```python
>>> s1 = 'abcd'
>>> s2 = 'efgh'
>>> id(s1)
2878933557800
>>> id(s2)
2878933558024
>>> s3 = s1 + s2
>>> id(s3)
2878932993776
>>> id(s1 + s2)
2878932993712
```
###### 建立由列表组成的列表  
使用列表推导式来建立嵌套列表
**示例2-10：一个包含3个列表的列表，嵌套的列表各自有三个元素**
```python
>>> borad = [['_'] * 3 for i in range(3)]
>>> borad
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> borad[1][2] = 'X'
>>> borad
[['_', '_', '_'], ['_', '_', 'X'], ['_', '_', '_']]
```
上面的代码等价于：
```python
>>> borad = []
>>> for i in range(3):
...     row = ['_'] * 3
...     borad.append(row)
... 
>>> borad
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> borad[2][0] = 'X'
>>> borad
[['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]
```
错误的捷径：
```python
>>> weird_board = [['_'] * 3] * 3
>>> weird_board
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
>>> weird_board[1][2] = 'O'
>>> weird_board
[['_', '_', 'O'], ['_', '_', 'O'], ['_', '_', 'O']]
```
上面错误的代码等价于：  
```python
>>>row=['_'] * 3
>>>board = []
>>>for i in range(3):
...    board.append(row)
```
**外面的列表其实是包含3个指向同一个列表的引用。**
