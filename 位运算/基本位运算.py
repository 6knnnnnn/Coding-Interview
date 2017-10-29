# -*- coding: utf-8 -*-


def reverse_bits(n):
    """
    https://leetcode.com/problems/reverse-bits/description/
    Reverse bits of a given 32 bits unsigned integer. 最简单的方式就是reverse bit string。
    对于一个number，向左移1位，变为number * 2，向右移1位，变为number / 2
    number & 1，得到的是最后一位本身，即 whatever1 & 1=1，whatever0 & 1 = 0
    所以如果是reverse 32位的，先左移结果，再累加上n的每一位bit 1/0
    可能的follow up，如果是有符号的？记住负号；如果需要call 很多次？
    """
    ans = 0
    for _ in xrange(32):
        ans <<= 1 # 左移结果，相当于 x 2
        ans += n & 1 # 加上当前n得对后一位
        n >>= 1 # 右移n，相当于 / 2
    return ans


def number_complement(x):
    """
    https://leetcode.com/problems/number-complement/description/
    把一个数X的bit位的数字flip，即01互换
    找到x的binary长度len，生成一个长度为的1111...111，然后异或运算XOR，即flip bit，时间O(N)
    """
    i = 1
    while i <= x:
        i <<= 1
    return (i-1) ^ x
