class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

l11 = ListNode(2)
l12 = ListNode(4)
l13 = ListNode(3)
l11.next = l12
l12.next = l13