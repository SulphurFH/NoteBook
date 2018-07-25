# -*- coding: utf-8 -*-


class Solution:
    """
    @param: : An integer
    @param: : An integer
    @return: An integer denote the count of digit k in 1..n
    """

    def digitCounts(self, k, n):
        # write your code here
        count = 0
        for i in xrange(n + 1):
            for j in str(i):
                if str(k) in j:
                    count += 1
        return count

s = Solution()
print s.digitCounts(1, 12)
