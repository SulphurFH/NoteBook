# -*- coding: utf-8 -*-

"""
给出数组 [9,3,2,4,8]，第三大的元素是 4
给出数组 [1,2,3,4,5]，第一大的元素是 5，第二大的元素是 4，第三大的元素是 3，以此类推
"""


class Solution:
    # @param k & A a integer and an array
    # @return ans a integer
    def kthLargestElement(self, k, A):
        def quickSort(A):
            less = []
            privotList = []
            more = []

            if len(A) <= 1:
                return A
            else:
                privot = A[0]
                for i in A:
                    if i < privot:
                        less.append(i)
                    elif i > privot:
                        more.append(i)
                    else:
                        privotList.append(i)

                less = quickSort(less)
                more = quickSort(more)
                return more + privotList + less

        result = quickSort(A)
        return result[k - 1]


A = [1, 2, 3, 4, 5]
k = 1
s = Solution()
print s.kthLargestElement(k, A)
