# -*- coding: utf-8 -*-


def search_for_range(nums, key):
    """
    https://leetcode.com/problems/search-for-a-range/description/
    nums已经是排序数组，找到nums中对应key的index range，不存在则返回[-1, -1]
    比如，[5, 7, 7, 8, 8, 10] key=8，结果为[3, 4]
    二分查找，找到key之后，缩小查找范围，分别查找左边和右边
    """
    def binary_search(nums, start, end, key):
        while 0 <= start <= end < len(nums):
            mid = (start + end) >> 1
            if nums[mid] == key:
                return mid
            if nums[mid] > key:
                end = mid - 1
            else:
                start = mid + 1
        return -1

    mid = binary_search(nums, 0, len(nums) - 1, key)
    index_range = [mid, mid]
    # key不存在，返回[-1, -1]
    if mid == -1:
        return index_range
    # [0...mid-1, mid, mid+1, ...len(nums)-1], mid = key
    # 分左右分别查找，即左边的结束end_l，右边的开始start_r
    end_l, start_r = mid - 1, mid + 1
    while end_l >= 0:
        mid_l = binary_search(nums, 0, end_l, key)
        if mid_l != -1:  # find key in left side, 即为index_range[0]
            index_range[0] = mid_l
            end_l = mid_l - 1
        else:
            break
    while start_r <= len(nums)-1:
        mid_r = binary_search(nums, start_r, len(nums) - 1, key)
        if mid_r != -1:  # find key in right side, 即为index_range[1]
            index_range[1] = mid_r
            start_r = mid_r + 1
        else:
            break
    return index_range
