# -*- coding: utf-8 -*-

import sys


def increasing_triplet_subsequence(nums):
    """
    https://leetcode.com/problems/increasing-triplet-subsequence/description/
    找到一个乱序数组中，是否存在三个数满足 i < j < k  且对应位置的数字是升序的，如何做到时间O(N)空间O(1)
    用两个变量first second表示i j，也就是保证 first < second，那么如果能找到第3个数，就说明存在
    从头开始遍历所有数字，遍历到数字n的时候，如果还没有return True，说明还没找到3个数字，最多只有first 和 second而已
    如果数字n比first要小，更新first，因为n更小，n后边的数字能找到满足条件的三个数机会更大
    如果比first大但是比second小，因为first肯定是在n之前的（而second不一定在first之前，以为有可能更新了first），更新second
    如果比first和second都大，找到了一种可能，返回True
    """
    first = second = sys.maxint
    for n in nums:
        if n <= first:
            first = n
        elif n <= second:
            second = n
        else:
            return True
    return False
