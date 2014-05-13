### Summary

用underscore(lodash) at javascript, 非常爽! 相似的方法如果用Python来实现怎么搞？！

- [ ] - 利用 ipython notebook 更好的 programable note 体验(边笔记，边写和跑 code snippets)
- [ ] - 看看 fn.py Functional programming in Python: implementation of missing features to enjoy FP


### Study

10. Functional Programming Modules
The modules described in this chapter provide functions and classes that support a functional programming style, and general operations on callables.

The following modules are documented in this chapter:

10.1. itertools — Functions creating iterators for efficient looping
10.2. functools — Higher-order functions and operations on callable objects
10.3. operator — Standard operators as functions



short functional paradigm presentation
disel popular myths about FP
characterize Python & FP relations
how can i make code better?


名词：
优点： avoid state, immutable data
first-class functions, higher-order functions, pure functions
recursion, tail recursion
iterators, seuquences, lazy evaluation(using generators?), pattern matching, monads...
map, reduce, filter - 三个高阶函数

调用方式， 是通过管道的方式联起来 - apply transformation(and compsitions) 转换和合成

```shell
echo "Daily active at, reply by, forum, user unique count"
cat logfile.log |grep '2013-11-14'|grep 'RAB'|awk '{print $10}'|sort|uniq -c|awk 'END{print NR}'
```

```python
from operator import add
expr = "28+32+++32++39"
print reduce(add, map(int, filter(bool, expr.split("+"))))
```
"28+32+++32++39"
["28","32","","","32","","39"]
["28","32","32","39"]
[28,32,32,39]
131


operator模块
把一些expression转成function invoke，这样chainable

```
operator.abs               operator.ilshift           operator.le
operator.add               operator.imod              operator.lshift
operator.and_              operator.imul              operator.lt
operator.attrgetter        operator.index             operator.methodcaller
operator.concat            operator.indexOf           operator.mod
operator.contains          operator.inv               operator.mul
operator.countOf           operator.invert            operator.ne
operator.delitem           operator.ior               operator.neg
operator.delslice          operator.ipow              operator.not_
operator.div               operator.irepeat           operator.or_
operator.eq                operator.irshift           operator.pos
operator.floordiv          operator.isCallable        operator.pow
operator.ge                operator.isMappingType     operator.repeat
operator.getitem           operator.isNumberType      operator.rshift
operator.getslice          operator.isSequenceType    operator.sequenceIncludes
operator.gt                operator.is_               operator.setitem
operator.iadd              operator.is_not            operator.setslice
operator.iand              operator.isub              operator.sub
operator.iconcat           operator.itemgetter        operator.truediv
operator.idiv              operator.itruediv          operator.truth
operator.ifloordiv         operator.ixor              operator.xor
```

itertools模块
this module implements a number of iterator building blocks. - functions craeting iterators for efficient

```
itertools.chain                          itertools.imap
itertools.combinations                   itertools.islice
itertools.combinations_with_replacement  itertools.izip
itertools.compress                       itertools.izip_longest
itertools.count                          itertools.permutations
itertools.cycle                          itertools.product
itertools.dropwhile                      itertools.repeat
itertools.groupby                        itertools.starmap
itertools.ifilter                        itertools.takewhile
itertools.ifilterfalse                   itertools.tee
```


dict(zip(map(lambda x:x["id"], items), items))

izip(imap(attrgetter('name'), items), items)

After f = attrgetter('name.first', 'name.last'), the call f(b) returns (b.name.first, b.name.last).



```python
list(itertools.imap(pow, (2,3,10), (5,2,3)))
dict(itertools.izip("ABCD", [1,2,3,4]))


def dropwhile(predicate, iterable):
    # dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
    iterable = iter(iterable)
    for x in iterable:
        if not predicate(x):
            yield x
            break
    for x in iterable:
        yield x

def izip(*iterables):
    # izip('ABCD', 'xy') --> Ax By
    iterators = map(iter, iterables)
    while iterators:
        yield tuple(map(next, iterators))

def imap(function, *iterables):
    # imap(pow, (2,3,10), (5,2,3)) --> 32 9 1000
    iterables = map(iter, iterables)
    while True:
        args = [next(it) for it in iterables]
        if function is None:
            yield tuple(args)
        else:
            yield function(*args)

class groupby(object):
    # [k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
    # [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D
    def __init__(self, iterable, key=None):
        if key is None:
            key = lambda x: x
        self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()
    def __iter__(self):
        return self
    def next(self):
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
        self.tgtkey = self.currkey
        return (self.currkey, self._grouper(self.tgtkey))
    def _grouper(self, tgtkey):
        while self.currkey == tgtkey:
            yield self.currvalue
            self.currvalue = next(self.it)    # Exit on StopIteration
            self.currkey = self.keyfunc(self.currvalue)
```


sorted, map, slice, reduce, iter, enumerate, reversed, 

```python
with open('mydata.txt') as fp:
    for line in iter(fp.readline, ''):
        process_line(line)
```
sorted(iterable[, cmp[, key[, reverse]]])
>>> sorted("This is a test string from Andrew".split(), key=str.lower)
['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']

>>> sorted(student_objects, key=lambda student: student.age) 


Tips:
avoid lopps using recursion

```python
def get_name():
    name = raw_input()
    return name if len(name) > 2 else get_name()

map(lambda x: x^2, [1,2,3,4,5])

def calculations(a, b):
    def add():
        return a + b

    return a, b, add

# function returns function as result or suing decorator syntax
def speak(topic):
    print "My speach is " + topic


def timer(fn):
    def inner(*args, **kwargs):
        t = time()
        fn(*args, **kwargs)
        print "took {time}".format(time=time()-t)

    return inner

speaker = timer(speak)
speaker("FP with Python")


partial function:
the process of fixing a number of arguments to a function, producing another function of samller arity

```python
def log(level, msg):
    print "[{level}]: {msg}".format(level=level, msg=msg)

def debug(msg):
    log('debug', msg)

# OR
from functools import partial
debug = partial(log, "debug")


# currying
# transforming a function that takes multiple arguments in such as way that it can be called as a chain of functions each with a signle argument
def fsum(f):
    def apply(a, b):
        return sum(map(f, range(a, b+1)))
    return apply

fsum(functools.partial(operator.mul, 2))(1, 10)

from operator import itemgetter
itemgetter(3)([1,2,3,4])

methodcaller("keys")(dict(name="Alexey", topic="FP"))

>>> methodcaller("count", 1)([1,1,1,2,2]) 
>>> # same as [1,1,1,2,2].count(1)

# Good function is small function
>>> ss = ["UA", "PyCon", "2012"]
>>> reduce(lambda acc, s: acc + len(s), ss, 0)

reduce(operator.add, map(len, ss))


# Python Hints
## types are callable
## classes are callable
## instance methods are callable
map(str, range(5))

>>> class Speaker(object):
...     def __init__(self, name):
...         self.name = name
>>> map(Speaker, ["Alexey", "Andrey", "Vsevolod"])
[<__main__.Speaker>, <__main__.Speaker>, <__main__.Speaker>]


```

Think Functional: Classes and OOP

mutable dict + partial binding
stop writing classes -> pycon us2012 - simplify your code, avoiding classes

```python
def ask(self, question):
    print "{name}, {q}?".format(name=self["name"], q=question)

def talk(self):
    print "I'm starting {topic}".format(topic=self["topic"])

from functools import partial
def cls(**methods):
    def bind(self):
        return lambda (name, method): (name, partial(method, self))
    return lambda **attrs: dict(
        attrs.items() + map(bind(attrs.copy()), methods.items())
    )

Speaker = cls(ask=ask, talk=talk)

def dct(*items):
    def pair((key, value)):
        return lambda k: value if k == key else None

    def merge(l, r):
        return lambda k: l(k) or r(k)

    return reduce(merge, map(pair, items), pair(None, None))


```


#### 总结

WHAT DID WE MISS? - ALMOST EVERTHING
Errors handling without exceptions
Pattern matching
Message passing
Fucntional data structures `cool`
Custom data types
Lazy evaluation


CON
No pattern matching syntax
Classes-based only type system
No functions overloading mechanism
Functions composition is not implemented in stdlib
Imperative errors handling based on exceptions






### 探索

#### pluck




### Raw Data
```python
users = [{
    "name" : "Bemmu",
    "uid" : "297200003"
},
{
    "name" : "Zuck",
    "uid" : "4"
}]
```

