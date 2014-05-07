## Special method

### Attribute Related
- object.__getattr__(self, name)
- object.__setattr__(self, name, val)
- object.__delattr__(self, name)
- object.__getattribute__(self, name)
- object.__get__(self, instance, owner)
- object.__set__(self, instance, value)
- object.__delete__(self, instance)


invoking descriptors
a descriptor is an object attribute with “binding behavior”, one whose attribute access has been overridden by methods in the descriptor protocol: __get__(), __set__(), and __delete__().
The property() function is implemented as a data descriptor. 
__slots__