# -*- coding: utf-8 -*-
from collections import defaultdict


def findLongestPalidrome(s):
    # 给一个字符串，求用其中字符组成的最长的回文字符串（如有多解，给一个答案即可）
    # 如"aabb"就是"abba","aabcbcd"就是"abcdcba"
    cc = defaultdict(int)
    for c in s:
        cc[c] += 1
    leftPart = []
    midChar = ''
    for c, count in cc.items():
        leftPart.append(c * (count / 2))
        if count % 2 != 0:
            # odd numbers count char, update midChar
            midChar = c
    return '{}{}{}'.format(''.join(leftPart), midChar, ''.join(leftPart[::-1]))

print findLongestPalidrome('aabb')
print findLongestPalidrome('aabbccddde')

