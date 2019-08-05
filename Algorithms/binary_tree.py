#!/usr/bin/python
# -*- coding: utf-8 -*-

class BinaryNode(object):
    def __init__(self, elem):
        self.elem = elem
        self.lchild = None
        self.rchild = None


class BinaryTree(object):
    def __init__(self):
        self.root = None
        self.nodeQueue = []

    def add(self, item):
        node = BinaryNode(item)
        if self.root is None:
            self.root = node
            self.nodeQueue.append(node)
        else:
            pop_node = self.nodeQueue.pop(0)
            if pop_node.lchild is None:
                pop_node.lchild = node
                self.nodeQueue.append(node)
                self.nodeQueue.insert(0, pop_node)
                return
            else:
                pop_node.rchild = node
                self.nodeQueue.append(node)
                return

    def front(self, root):
        if not root:
            return
        print root.elem,
        self.front(root.lchild)
        self.front(root.rchild)

    def middle(self, root):
        if not root:
            return
        self.middle(root.lchild)
        print root.elem,
        self.middle(root.rchild)

    def later(self, root):
        if not root:
            return
        self.later(root.lchild)
        self.later(root.rchild)
        print root.elem,

    def level(self, root):
        if not root:
            return
        q = []
        q.append(root)
        while q:
            node = q.pop(0)
            print node.elem,
            if node.lchild:
                q.append(node.lchild)
            if node.rchild:
                q.append(node.rchild)


if __name__ == '__main__':
    nodeList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    binaryTree = BinaryTree()
    for node in nodeList:
        binaryTree.add(node)

    binaryTree.level(binaryTree.root)
    print ''
    binaryTree.front(binaryTree.root)
    print ''
    binaryTree.middle(binaryTree.root)
    print ''
    binaryTree.later(binaryTree.root)
    print ''
    print binaryTree.nodeQueue
