class Solution(object):
    @staticmethod
    def longestPalindrome(s):
        """
        :type s: str
        :rtype: str
        """
        sum = 0
        d = {}
        start = 0
        end = 0
        for i, ch in enumerate(s):
            if ch in d and i - d[ch] + 1 > sum:
                start = d[ch]
                end = i
                sum = i - d[ch] + 1
            d[ch] = i
        return s[start:end + 1]

print Solution.longestPalindrome('abacccba')