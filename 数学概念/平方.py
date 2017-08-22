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
