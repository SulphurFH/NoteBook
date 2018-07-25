# -*- coding: utf-8 -*-

def singleton(cls, *args, **kwargs):
    instance = {}
    
    def wrapper():
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper


@singleton
class MyClass(object):
    a = 1

a = MyClass()
b = MyClass()

print id(a)
print id(b)
