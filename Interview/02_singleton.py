# -*- coding: utf-8 -*-


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MyClass(Singleton):
    a = 1


a = MyClass()
b = MyClass()

print id(a)
print id(b)
