# 单例模式

## __metaclass__

```
class Singleton(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instance:
            Singleton._instance[cls] = type.__call__(cls, *args, **kwargs)
        return Singleton._instance[cls]

class A(object):
    __metaclass__ = Singleton

a1 = A()
a2 = A()
print id(a1) == id(a2)
```

## __new__

```
# -*- coding: utf-8 -*-


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MyClass(Singleton):
    a = 1
```

## 装饰器

```
# -*- coding: utf-8 -*-


def get_single_instance(cls, *args, **kwargs):
    instance = {}

    def wrapper():
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return wrapper


@get_single_instance
class MyClass(object):
    a = 1
```

# 生产者消费者

## 线程

```
# -*- coding: utf-8 -*-
import time
from threading import Thread, Condition


class Producer(Thread):
    def run(self):
        global count
        while True:
            if con.acquire():
                if count > 1000:
                    con.wait()
                else:
                    count += 100
                    print self.name + " prudce 100, count = " + str(count)
                    con.notify()
                con.release()
            time.sleep(1)


class Consumer(Thread):
    def run(self):
        global count
        while True:
            if con.acquire():
                if count < 100:
                    con.wait()
                else:
                    count -= 3
                    print self.name + " Consumer 3, count = " + str(count)
                    con.notify()
                con.release()
            time.sleep(1)


if __name__ == "__main__":
    count = 500
    con = Condition()

    for i in range(2):
        p = Producer()
        p.start()

    for i in range(5):
        c = Consumer()
        c.start()
```

# 二分查找

```
# -*- coding: utf-8 -*-


def binarySearch(l, t):
    low, high = 0, len(l) - 1
    while low < high:
        mid = (low + high) / 2
        if l[mid] > t:
            high = mid
        elif l[mid] < t:
            low = mid + 1
        else:
            return mid
    return -1 

if __name__ == '__main__':
    l = [1, 4, 12, 45, 66, 99, 120, 444]
    print binarySearch(l, 99)
```

# 斐波那契数列

```
def fib(n):
    a, b = 0, 1
    for _ in xrange(n):
        a, b = b, a + b
    return b
```

```
fib = lambda n: n if n<=2 else fib(n - 1) + fib(n - 2)
```


# 去除列表中的重复元素

## 用集合

```
list(set(l))
```

## 用字典

```
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = {}.fromkeys(l1).keys()
```

## 用字典并保持顺序

```
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = list(set(l1))
l2.sort(key=l1.index)
```

## 列表推导式

```
l1 = ['b','c','d','b','c','a','a']
l2 = []
[l2.append(i) for i in l1 if i not in l2]
print l2
```

# 合并两个有序列表

## 尾递归

```
# -*- coding: utf-8 -*-


def _recursion_merge_sort2(l1, l2, tmp):
    if len(l1) == 0 or len(l2) == 0:
        tmp.extend(l1)
        tmp.extend(l2)
        return tmp
    else:
        if l1[0] < l2[0]:
            tmp.append(l1[0])
            del l1[0]
        else:
            tmp.append(l2[0])
            del l2[0]
        return _recursion_merge_sort2(l1, l2, tmp)


def recursion_merge_sort2(l1, l2):
    return _recursion_merge_sort2(l1, l2, [])
```

# 冒泡

```
# -*- coding: utf-8 -*-


def bubbleSort(lists):
    count = len(lists)
    for i in range(0, count):
        for j in range(i + 1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    return lists
```

# 插入排序

```
# -*- coding: utf-8 -*-


def insert_sort(lists):
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            j -= 1
    return lists
```

# 快排

## 递归

```
# -*- coding: utf-8 -*-


def qsort(seq):
    if seq == []:
        return []
    else:
        pivot = seq[0]
        lesser = qsort([x for x in seq[1:] if x < pivot])
        greater = qsort([x for x in seq[1:] if x >= pivot])
        return lesser + [pivot] + greater


if __name__ == "__main__":
    seq = [5, 6, 78, 9, 0, -1, 2, 3, -65, 12]
    print qsort(seq)
```

# 遍历二叉树

```
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))


def lookup(root):
    """
    层次遍历
    """
    stack = [root]
    while stack:
        current = stack.pop(0)
        print current.data
        if current.left:
            stack.append(current.left)
        if current.right:
            stack.append(current.right)


def deep(root):
    """
    深度遍历
    """
    if not root:
        return
    print root.data
    deep(root.left)
    deep(root.right)


def maxDepth(root):
    """
    求最大树深
    """
    if not root:
        return 0
    return max(maxDepth(root.left), maxDepth(root.right)) + 1


def isSameTree(tree_one, tree_two):
    if not tree_one and not tree_two:
        return True
    elif tree_one and tree_two:
        return tree_one.data == tree_two.data and isSameTree(tree_one.left, tree_two.right) and isSameTree(tree_one.right, tree_two.right)
    else:
        return False


if __name__ == "__main__":
    # lookup(tree)
    # deep(tree)
    maxDepth(tree)
```
