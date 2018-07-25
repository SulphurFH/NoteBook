# -*- coding: utf-8 -*-

"""
删除链表中等于给定值val的所有节点。
给出链表 1->2->3->3->4->5->3, 和 val = 3, 你需要返回删除3之后的链表：1->2->4->5。
"""

"""
Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
"""


class Solution:
    """
    @param: head: a ListNode
    @param: val: An integer
    @return: a ListNode
    """

    def removeElements(self, head, val):
        # Write your code here
        if head is None:
            return None
        pre = head
        while pre.next:
            if pre.next.val == val:
                pre.next = pre.next.next
            else:
                pre = pre.next
        if head.val == val:
            return head.next
        return head
