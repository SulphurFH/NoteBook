class Solution:
    """
    @param: a: An integer
    @param: b: An integer
    @return: The sum of a and b
    """

    def aplusb(self, a, b):
        # write your co
        def add(num1, num2):
            sum = num1 ^ num2
            carry = (num1 & num2) << 1
            while (carry != 0):
                num1 = sum
                num2 = carry
                sum = num1 ^ num2
                carry = (num1 & num2) << 1
            return sum

        if a == 0 and b == 0:
            return 0
        subtractor = add(~a, 1)
        if subtractor == b:
            return 0
        else:
            return add(a, b)


s = Solution()
print s.aplusb(0, 0)
