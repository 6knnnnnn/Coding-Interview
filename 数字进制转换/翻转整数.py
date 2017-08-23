# -*- coding: utf-8 -*-

"""
10进制转换为k进制：num %k 就是digit的最后一位数字，num / k 就是num整体往右移动一个digit的结果
但只能是10进制，因为% / 运算都是对于十进制而言的。
"""


def reverse_integer(x):
    pos = True if x >= 0 else False
    x = y = 0
    while x != 0:
        y = y * 10 + x % 10
        x = x / 10

    return y if pos else -y


def add_digits_until_single_one(num):
    # https://leetcode.com/problems/add-digits/description/
    pass