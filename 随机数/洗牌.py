# -*- coding: utf-8 -*-

from random import sample


class Shuffle(object):
    # https://leetcode.com/problems/shuffle-an-array/description/
    def __init__(self, nums):
        self.nums = nums
        self.total = len(self.nums)

    def reset(self):
        return self.nums

    def shuffle(self):
        # Returns a random shuffling of the array.
        # 需要时间空间复杂度O(N)
        return sample(self.nums, len(self.nums))

sol = Shuffle(range(10))

for i in xrange(10):
    print sol.shuffle()
