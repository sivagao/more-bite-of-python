

```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, _observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

class Data(Subject):
    def __init__(self, name=''):
        Subject.__init__(self)
        self.name = name
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify()

class HexViewer:
    def update(self, subject):
        print "HexViewer: Subject %s has data %d" % (subject.name, subject.data)

class DecimalViewer:
    def update(self, subject):
        print "DecimalViewer: Subject %s has data %d" % (subject.name, subject.data)

def main():
    data1 = Data('Data 1')
    data2 = Data('Data 2')


```