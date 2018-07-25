# coding=utf8

class Solution(object):
    @staticmethod
    def lengthOfLongestSubstring(s):
        """
        :type s: str
        :rtype: int
        """
        xList = []
        maxLen = 0
        for x in s:
            xList.append(x)
            if len(xList) != len(set(xList)):
                xList = xList[xList.index(x) + 1 :]
            maxLen = max(maxLen, len(xList))
        return maxLen
    @staticmethod
    def lengthOfLongestSubstring2(s):
        sum = 0  
        left = 0  
        d = {}  
  
        for i, ch in enumerate(s):  
            if ch in d and d[ch] >= left:  
                left = d[ch] + 1  
            d[ch] = i  
            sum = max(sum, i - left + 1)  
            import pdb;pdb.set_trace()
        return sum

# print Solution.lengthOfLongestSubstring('bbbbabaaaaaabwcbbb')
print Solution.lengthOfLongestSubstring2('abcabcde')