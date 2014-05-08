### TODO:
- [ ] 想想更好的例子，妈蛋例子都太挫了！

```python
def concreteDraw1():
    print "concreteDraw1"

def concreteDraw2():
    print "concreteDraw2"

class Circle:
    def __init__(self, method):
        self.method = method

    def draw(self):
        self.method()

def main():
    circles = (Circle(concreteDraw1), Circle(concreteDraw1))

    for i in circles:
        i.draw()

if __name__ == "__main__":
    main()

```