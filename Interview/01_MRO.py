# -*- coding: utf-8 -*-


class A():
    def foo1(self):
        print("A")


class B(A):
    def foo2(self):
        pass


class C(A):
    def foo1(self):
        print("C")


class D(B, C):
    pass


d = D()
d.foo1()

# 2A
# 3C
