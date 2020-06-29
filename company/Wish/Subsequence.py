# -*- coding: utf-8 -*-
from collections import deque


def longest_increasing_subsequence(nums):
    # https://leetcode.com/problems/longest-increasing-subsequence/
    pass


def longest_consecutive_sequence(nums):
    # 排序 or 用hash set记录
    longest = 0
    num_set = set(nums)
    num_checked = set([])
    for num in num_set:
        if num not in num_checked:
            num_checked.add(num)
            if num - 1 not in num_set:
                # find a new one
                current_length = 1
                while num + 1 in num_set:
                    num += 1
                    current_length += 1
                    num_checked.add(num)
                longest = max(longest, current_length)
    return longest


def longest_mountain_in_array(nums):
    # https://leetcode.com/problems/longest-mountain-in-array/
    # 左边一直在increasing 右边一直在decreasing
    def findIncreasingRange(nums, i):
        while i < len(nums) - 1 and nums[i] < nums[i + 1]: i += 1
        return i

    def findDecreasingRange(nums, j):
        while j < len(nums) - 1 and nums[j] > nums[j + 1]: j += 1
        return j

    longest = 0
    # mountains = []
    if nums:
        i = 0
        while i < len(nums):
            j = findIncreasingRange(nums, i)
            if j < len(nums) - 1:
                break
            k = findDecreasingRange(nums, j)
            if i < j < k:
                # mountains.append(nums[i:k + 1])
                longest = max(longest, k - i + 1)
            # update i as either k or i+1 if k == i
            i = max(i+1, k)
    return longest


def test1():
    for nums in [
        [2, 2, 2],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [2, 1, 4, 7, 3, 2, 5, 1, 2, 3, 2, 1, 5, 2],
    ]:
        print longest_mountain_in_array(nums)


def shortestSubarray(nums, k):
    i = total = 0
    while i < len(nums) and total < k:
        total += nums[i]
        i += 1
    # find the first window that might be the shortest subarray
    if i == len(nums):
        return -1 if total < k else i
    shortestSize = i
    queue = deque([nums[:i]])
    total = 0
    while i < len(nums):
        # no need to consider this negative or zero num as it contributes nothing
        if nums[i] <= 0:
            while i < len(nums) and nums[i] <= 0:
                i += 1
            # reset total sum
            total = 0
            queue = deque([])
        else:
            # now find a pos number
            inNum = nums[i]
            outNum = queue[0]
            if inNum <= 0:
                pass

    return shortestSize