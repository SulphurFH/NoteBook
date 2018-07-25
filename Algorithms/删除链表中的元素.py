#!/usr/bin/python
# -*- coding: utf-8 -*-

class Node(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class LinkList(object):
    def __init__(self):
        self.head = None

    def initList(self, data):
        self.head = Node(data[0])
        p = self.head

        for i in data[1:]:
            node = Node(i)
            p.next = node
            p = p.next

    def removeElements(self, val):
        while True:
            if self.head and self.head.val == val:
                self.head = self.head.next
            else:
                break

        if self.head is None:
            return

        t = self.head
        p = self.head.next
        while True:

            if p.val == val:
                t.next = p.next
            else:
                t = p
            if p.next is None:
                return
            p = p.next


    def printLinkList(self):
        l = []
        if self.head is None:
            return
        temp = self.head
        while True:
            l.append(temp.val)
            if not temp.next:
                break
            temp = temp.next
        print l
        return


nodeList = [3, 3, 1, 2, None, None, 3, 3, 4, 5, 3, 3, None]
nodeList = [5, None]
l = LinkList()
l.initList(nodeList)
l.removeElements(3)
l.printLinkList()
