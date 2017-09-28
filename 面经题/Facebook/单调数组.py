# -*- coding: utf-8 -*-


"""
判断一个数组是否是单调的，也就是，是否满足单调递增，或者单调递减，或者单调不变
用两个flag，表明是存在递增或者递减的情况，即nums[i]<nums[j] 或者 nums[i]>nums[j]

如果遍历结束后，最后都为True，说明同时存在递增和递减的情况，所以不单调。
否则，至少其中有一个为False，那么就满足单调。即要么单调递增或者递减，要么所有的值都相等。
[1, 1, 2] True  [1, 0, -1] True [1, 1, 1] True [1, 2, 1] False
"""


def monotonic_array(nums):
    d = a = False
    for i in xrange(len(nums)-1):
        d = nums[i-1] > nums[i]
        a = nums[i-1] < nums[i]
    if d and a:
        return False
    return True
