# -*- coding: utf-8 -*-


class Solution:
    """
    @param: n: An integer
    @return: An integer, denote the number of trailing zeros in n!
    """

    def trailingZeros(self, n):
        # write your code here, try to do it without arithmetic operators.
        ret = 0
        while n:
            ret += n / 5
            n /= 5
        return ret


s = Solution()
print s.trailingZeros(105)
