"""
Input: "Hello World"
Output: "olleH dlroW"
"""
"""
Input: "Hello World"
Output: "World Hello"
"""
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        return ' '.join([x[::-1] for x in s.split(' ')])

    def reverseWords2(self, s):
        """
        :type s: str
        :rtype: str
        """
        return ' '.join([x for x in s.split(' ')][::-1])

if __name__ == '__main__':
    s = Solution()
    print s.reverseWords("Hello World")
    print s.reverseWords2("Hello World")
