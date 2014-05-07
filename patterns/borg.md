### TODO:
- [ ] 想想更好的例子，这个技巧的应用场景?

### Tips
- object.__dict__: A dictionary or other mapping object used to store an object’s (writable) attributes.
- Variables declared inside the class definition, but not inside a method are class or static variables
- @classmethod 和 @staticmethod的区别： advantages of @classmethod over @staticmethod AFAIK is that you always get the name of the class the method was invoked on, even if it's a subclass?
- borg的意思： 吸收同化一切？！

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Borg:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = 'Init'

    def __str__(self):
        return self.state


class YourBorg(Borg):
    pass

if __name__ == '__main__':
    def tell_state(rm1, rm2):
        print('rm1: {0}'.format(rm1))
        print('rm2: {0}'.format(rm2))
        if rm1.another_state:
            print('rm1: {0}'.format(rm1.another_state))
            print('rm2: {0}'.format(rm2.another_state))

    rm1 = Borg()
    rm2 = YourBorg()

    rm1.another_state = 'Init'
    tell_state(rm1, rm2)

    rm2.state = 'Running'
    rm1.another_state = 'Zoombie'
    tell_state(rm1, rm2)

```