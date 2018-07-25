# -*- coding: utf-8 -*-


class Solution:
    """
    @param: nums: a list of integers
    @return: The majority number that occurs more than 1/3
    """

    def majorityNumber(self, nums):
        # write your code here
        length = len(nums)
        need_count = length / 3
        if length % 3 != 0:
            need_count += 1
        nums_dict = {}
        for i in nums:
            if i in nums_dict.keys():
                nums_dict[i] += 1
            else:
                nums_dict[i] = 1
        for i, j in nums_dict.items():
            if j >= need_count:
                return i


nums = [1, 2, 1, 2, 1, 3, 3]
s = Solution()
print s.majorityNumber(nums)
