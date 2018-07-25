"""
A happy number is a number defined by the following process: Starting with any positive integer, 
replace the number by the sum of the squares of its digits, 
and repeat the process until the number equals 1 (where it will stay), 
or it loops endlessly in a cycle which does not include 1. 
Those numbers for which this process ends in 1 are happy numbers.

Example: 19 is a happy number
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1
"""
class Solution1(object):
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        nlist = []
        while True:
            if n in nlist or n == 1:
                return True if n == 1 else False
            nlist.append(n)
            n = self.sumOfSquare(n)
    
    def sumOfSquare(self, n):
        result = 0
        for x in str(n):
            result += int(x) * int(x)
        return result

class Solution2(object):
    def isHappy(self, n, nlist):
        if n in nlist or n == 1:
            return True if n == 1 else False
        # import pdb;pdb.set_trace()
        nlist.append(n)
        a = 0
        for x in str(n):
            a += int(x) ** 2
        n = a
        return self.isHappy(n, nlist)


if __name__ == '__main__':
    
    s1 = Solution1()
    print s1.isHappy(19)
    print s1.isHappy(58)

    s2 = Solution2()
    print s2.isHappy(19, [])
    print s2.isHappy(58, [])