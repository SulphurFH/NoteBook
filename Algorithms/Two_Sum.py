"""
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
"""

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        d={}
        for i in range(len(nums)):
            if d.has_key(nums[i]):
                return [d[nums[i]],i]
            else:
                bal = target - nums[i]
                d[bal] = d.get(bal,i)

if __name__ == '__main__':
    s = Solution()
    print s.twoSum([3, 2, 4], 6)