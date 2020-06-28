# -*- coding: utf-8 -*-


def longest_mountain_in_array(nums):
    # https://leetcode.com/problems/longest-mountain-in-array/
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
