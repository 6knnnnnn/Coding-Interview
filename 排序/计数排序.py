# -*- coding: utf-8 -*-


def sort_colors(nums):
    """
    https://leetcode.com/problems/sort-colors/description/
    荷兰国旗问题，0、1、2分别表示红白蓝，按照红白蓝依次排序
    counting sort，按照每一位置排序，每一位的顺序需要预先定义好
    """
    count_array = [0, 0, 0]
    color_array = [0, 1, 2]
    for n in nums:
        count_array[n] += 1
    i = j = 0 # 两个pointers，i指向nums，j指向color count
    while i < len(nums):
        while j < len(count_array) and count_array[j] > 0:
            count_array[j] -= 1
            nums[i] = color_array[j] # 找到对应颜色
            i += 1
        j += 1
