# -*- coding: utf-8 -*-


def sum_of_square_number(c):
    # https://leetcode.com/problems/sum-of-square-numbers/description/
    # 判断 a^2 + b^2 = c，可以为0，暴力解法，a从0到c的平方根的ceiling，b^2为c-a^2，
    # 然后求平方根的flooring，再取平方和判断是否为b^2本身
    for a in xrange(int(c ** 0.5) + 1):
        bb = c - a ** 2
        if int(bb ** 0.5) ** 2 == bb:
            return True
    return False


def valid_perfect_square(num):
    # https://leetcode.com/problems/valid-perfect-square/description/
    # 二分查找
    left = 0
    right = num
    while left <= right:
        mid = (left + right) >> 1
        sq_mid = mid ** 2
        if sq_mid > num:
            right = mid - 1
        elif sq_mid < num:
            left = mid + 1
        else:
            return True
    return False


def happy_number(num):
    """
    https://leetcode.com/problems/happy-number/description/
    所谓的happy number就是，每一位的digit的平方相加，组成新的数字，由此过程不断地loop，直到能够得到1为止，即最后不能够在loop了。
    或者回到某个中间状态，即产生cycle。用hash set记录历史，如果存在历史，返回False。
    Example: 19 is a happy number: 1^2 + 9^2 = 82, 8^2 + 2^2 = 68, 6^2 + 8^2 = 100, 1^2 + 0^2 + 0^2 = 1
    """
    d_set = set([])
    while num not in d_set:
        d_set.add(num)
        m = 0
        for i in str(num):
            m += int(i) ** 2
        if m == 1:
            return True
        num = m
    return False


def square_root(x):
    """
    https://leetcode.com/problems/sqrtx/description/
    求一个数字的平方根，Newton binary approximate approach，不断的逼近最后的平方根
    """
    left, right, ans = 1, x, 0
    while left <= right:
        mid = (left + right) >> 1
        if mid * mid <= x:
            left = mid + 1
            ans = mid
        else:
            right = mid - 1
    return ans
