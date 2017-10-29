# -*- coding: utf-8 -*-

"""
https://leetcode.com/problems/missing-ranges/description/
Given a sorted integer array where the range of elements are in the
inclusive range [lower, upper], return its missing ranges.
特殊情况：integer越界？
Test case1: [0, 1, 3, 50, 75], 2, 30 = ["2","4->49","51->74"]
            就是如果lower或者upper在input数组里面（是不是最大/小），那么就是原始数组的range
Test case2: [0, 1, 3, 50, 75], -10, 99 = ["-10->-1","2","4->49","51->74", "76->99"]
"""


def missing_ranges(A, lower, upper):
    result = []
    # 如果upper是最大的，要考虑到upper+1，inclusive
    # 即便不是最大，而是在A中间，那么之后比较的时候会忽略掉，因为真正的upper在最后
    A.add(upper + 1)
    # 如果lower是最小的，从lower-1开始考虑，inclusive
    # 即便不是最小，而是在A中间，那么之后比较的时候会忽略掉，因为真正的lower在最前
    prev = lower - 1
    for n in A:
        # 我们只考虑 n > prev 的情况，所以如果lower/prev > n or upper/n > prev，都会忽略
        # if n==prev+1, 一个都没少，连续的consecutive
        if n == prev + 2:
            # 少了一个[1， 3...] -> 2
            result.append(str(n - 1))
        elif n > prev + 2:  # 少了至少两个，即[prev+1, ..., n-1]
            result.append("%s->%s" % (prev + 1, n - 1))
        prev = n
    return result


def summary_range(nums):
    """
    https://leetcode.com/problems/summary-ranges/description/
    Given a sorted integer array without duplicates, return the summary of its ranges.
    Test case1: [0,1,2,4,5,7], return ["0->2","4->5","7"]
    Test case1: [1,2,3,4,5,6,7,8], return ["1->8"]
    """
    resL = []
    if nums:
        i, n = 0, len(nums)
        while i < n:
            start, end = nums[i], None
            while i < n - 1 and nums[i] + 1 == nums[i + 1]:
                end = nums[i + 1]  # 连续的，继续移动i
                i += 1
            # 如果有开始和结尾点, 否则单一变量
            resL.append("%s->%s" % (start, end) if end is not None else str(start))
            i += 1
    return resL

test1 = [0,1,2,4,5,7]
print test1, summary_range(test1)
test2 = range(10)
print test2, summary_range(test2)