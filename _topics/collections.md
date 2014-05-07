
### TODO:
- [ ] 优化格式

Creating containers and collections
ABCs of collections - list, dict, set, tuple
examples of special methods - 特殊方法
using the standard library extensions - (namedtuple, deque, ChainMap, OrderedDict, defaultDict, counter)
creating new kinds of collections
define a new kind of sequences
creating a new kind of mapping
creating a kind of set
summary





collections - container datatypes
namedtuple()factory function for creating tuple subclasses with named fieldsdequelist-like container with fast appends and pops on either endChainMapdict-like class for creating a single view of multiple mappingsCounterdict subclass for counting hashable objectsOrderedDictdict subclass that remembers the order entries were addeddefaultdictdict subclass that calls a factory function to supply missing valuesUserDictwrapper around dictionary objects for easier dict subclassingUserListwrapper around list objects for easier list subclassingUserStringwrapper around string objects for easier string subclassing



namedtuple - 非常不错， verbose模式也打印出了， 在映射sql和csv的时候很好用
Named tuples assign meaning to each position in a tuple and allow for more readable, self-documenting code. They can be used wherever regular tuples are used, and they add the ability to access fields by name instead of position index.
Point = namedtuple('Point', ['x', 'y'], verbose=True)


deque - double-ended queue
one way a deque is used it to “age” items. 如最近的50个history. 并且know the oldest and the newest items 是O(1)的复杂度
去实现一个waiting line : waiting line: entities (bits, people, cars, words, particles, whatever) arrive with a certain frequency to the end of the line and are serviced at a different frequency at the beginning of the line. While waiting some entities may decide to leave the line.... etc. The point is that you need "fast access" to insert/deletes at both ends of the line, hence a deque.
除了性能好以外，一个非常好用的特性是maxlength!!! oldest(leftest) item is popleft() 自动的如果超过maxlength
实现更多『粒子』操作：
To implement deque slicing, use a similar approach applying rotate() to bring a target element to the left side of the deque. Remove old entries with popleft(), add new entries with extend(), and then reverse the rotation. With minor variations on that approach, it is easy to implement Forth style stack manipulations such as dup, drop, swap, over, pick, rot, and roll.


deq = deque(range(500), 10)
deq.append(501)


ChainMap
A ChainMap class is provided for quickly linking a number of mappings so they can be treated as a single unit. It is often much faster than creating a new dictionary and running multiple update() calls.

import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))
环境， 命令行参数解析
combined = ChainMap(command_line_args, os.environ, defaults)




Counter - to provide convenient and rapid tallies.(点数)
cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
     cnt[word] += 1
Counter('gaohailang').most_common(3)



>>> c = Counter(a=3, b=1)
>>> d = Counter(a=1, b=2)
>>> c + d                       # add two counters together:  c[x] + d[x]
Counter({'a': 4, 'b': 3})
>>> c - d                       # subtract (keeping only positive counts)
Counter({'a': 2})



defaultdict
__missing__, default_factory: This attribute is used by the __missing__() method; it is initialized from the first argument to the constructor

d = defaultdict(list), 还可以是set,等factory_method

>>> s = 'mississippi'
>>> d = defaultdict(int)
>>> for k in s:
...     d[k] += 1

>>> d = {}
>>> for k, v in s:
...     d.setdefault(k, []).append(v)


orderedDict
默认的orderedDict的排序是： in the order their keys were first added

但在实例化时候，可以改变排序（传入sorted的list）：
In [11]: OrderedDict(sorted(d.items(), key=lambda t: -t[1]))
Out[11]: OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])

