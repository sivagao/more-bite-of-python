### TODO:
- [ ] 想想更好的例子，这个技巧的应用场景?
- [ ] Python default parameter 造成的问题 - 调用很不方便

### Tips
- "Least Astonishment" in Python: which scope is the Mutable Default Argument in?
code showcase:

```python
def foo(a=[]):
    a.append(5)
    return a
```

>>> foo()
[5]
>>> foo()
[5, 5]
the function keeps using the same object, in each call. The modifications we make are “sticky”.
Default parameter values are always evaluated when, and only when, the “def” statement they belong to is executed;
this is not a desing flaw, and it is not because of internals, or performance
it comes simply from that fact that functions in Python are first-class objects, not only a piece of code - a function is an object being evaluted on its definition; default paramerters are kinds of "member data" and therefore their state may change from one call to other

local caches/memoization:

```python
def calculate(a, b, c, memo={}):
    try:
        value = memo[a, b, c] # return already calculated value
    except KeyError:
        value = heavy_calculation(a, b, c)
        memo[a, b, c] = value # update the memo dictionary
    return value
```

```python
class GraphSearch:

    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start, end, path=[]):
        self.start = start
        self.end = end
        self.path = path
        self.path += [self.start]
        if self.start == self.end:
            return [self.path]
        if self.start not in self.graph:
            return []
        paths = []
        for node in self.graph[self.start]:
            if node not in self.path:
                newpaths = self.find_path(node, self.end, self.path)
                if newpaths:
                    return newpaths[0]
        return []

    def find_shortest_path(self, start, end, path=[]):
        # self.start = start
        # self.end = end
        # self.path = path
        # self.path += [self.start]
        # if self.start == self.end:
        #     return self.path
        # if self.start not in self.graph:
        #     return None
        # shortest = None
        # for node in self.graph[self.start]:
        #     if node not in self.path:
        #         newpath = self.find_shortest_path(node, self.end, self.path)
        #         if newpath:
        #             if not shortest or len(newpath) < len(shortest):
        #                 shortest = newpath
        # return shortest
        # or rewrite like this
        paths = self.find_all_path(start, end)
        print paths
        if paths:
            return sorted(paths, key=lambda p: len(p))[0]
        else:
            return None # transform [] to None

    def find_all_path(self, start, end, path=[]):
        self.start = start
        self.end = end
        self.path = path
        self.path += [self.start]
        if self.start == self.end:
            return [self.path]
        if self.start not in self.graph:
            return []
        paths = []
        for node in self.graph[self.start]:
            if node not in self.path:
                newpaths = self.find_all_path(node, self.end, self.path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

graph = {'A': ['B', 'C'],
        'B': ['C','D'],
        'C': ['D'],
        'D': ['C'],
        'E': ['F'],
        'F': ['C']}

graph1 = GraphSearch(graph)

print(graph1.find_path('A', 'D'))
print(graph1.find_all_path('A', 'D'))
# print(graph1.find_shortest_path('A', 'D'))
print(graph1.find_all_path('A', 'D'))
```
