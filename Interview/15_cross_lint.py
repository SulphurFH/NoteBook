# -*- coding: utf-8 -*-


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def node(l1, l2):
    length1, length2 = 0, 0
    # 求两个链表长度
    while l1.next:
        l1 = l1.next  # 尾节点
        length1 += 1
    while l2.next:
        l2 = l2.next  # 尾节点
        length2 += 1

    # 如果相交
    if l1.next == l2.next:
        # 长的链表先走
        if length1 > length2:
            for _ in range(length1 - length2):
                l1 = l1.next
            return l1  # 返回交点
        else:
            for _ in range(length2 - length1):
                l2 = l2.next
            return l2  # 返回交点
    # 如果不相交
    else:
        return
