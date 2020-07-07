# -*- coding: utf-8 -*-
from collections import deque


def longest_increasing_subsequence(nums):
    """
    https://leetcode.com/problems/longest-increasing-subsequence/
    https://www.cnblogs.com/grandyang/p/4938187.html
    dp[i] 表示在i位置时，可以找到的LIS的长度，初始dp[x] = 1，即每一个单个元素也可以当作是LIS不过size=1
    i >= 1 时候 dp[i]更新方式：
    1、找到0...i-1所有nums[j]，若nums[i]>nums[j], 说明i可以被加到以j为结尾的LIS当中，所以更新dp[i]为dp[j]+1
    2、处理完所有的0...i-1，找到其中最大的dp[j]+1的值
    所以每一个i，都要遍历之前的0...i-1，时间复杂度为O(N^2) 空间为O(N)
    """
    if not nums:
        return 0
    dp = []
    for i in xrange(len(nums)):
        # default value 1 since a single value is also a LIS
        dp.append(1)
        for j in xrange(i):
            if nums[i] > nums[j] and dp[j] + 1 > dp[i]:
                # find one candidate, record the index
                dp[i] = dp[j]+1
    return max(dp), dp


print longest_increasing_subsequence([1,4,3,2,6,5])


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
    mountains = []
    if nums:
        i = 0
        while i < len(nums):
            j = findIncreasingRange(nums, i)
            k = findDecreasingRange(nums, j)
            if i < j < k:
                mountains.append(nums[i:k + 1])
                longest = max(longest, k - i + 1)
            # update i as either k or i+1 if k == i
            i = max(i+1, k)
    return longest, mountains


def test1():
    for nums in [
        [2, 2, 2],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [2, 1, 4, 7, 3, 2, 5, 1, 2, 3, 2, 1, 5, 2],
    ]:
        print longest_mountain_in_array(nums)


test1()

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