# -*- coding: utf-8 -*-


def longest_consecutive_sequence(nums):
    # https://leetcode.com/problems/longest-consecutive-sequence/description/
    # 用hash set记录历史记录，每次找到一个数字，向前、后找连续的同时更新历史记录，每次更新结果max len
    # 所以有点像滑动窗口，向前向后滑
    # Sort 的解法也可以做，O(NlogN)，O(N)就需要hash set额外空间
    num_set = set(nums)
    max_len = 0
    for n in nums:
        if n not in num_set:
            continue
        curlen = 1
        forward, backward = n + 1, n - 1
        while forward in num_set:
            num_set.remove(forward)
            forward += 1
            curlen += 1
        while backward in num_set:
            num_set.remove(backward)
            backward -= 1
            curlen += 1
        max_len = max(max_len, curlen)
    return max_len


def longest_consecutive_sequence2(nums):
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
    pass