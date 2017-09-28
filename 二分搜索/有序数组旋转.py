# -*- coding: utf-8 -*-


def search_in_rotated_sorted_array(nums, target):
    """
    https://leetcode.com/problems/search-in-rotated-sorted-array/description/
    某个原本排序的数组被旋转了一次，给定一个数字，找到这个数组中是否存在以及对应的index，不存在则返回-1

    """
    if not nums:
        return -1
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) / 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:
            # sorted order
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # drop between low, high
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return lo if nums[lo] == target else -1


