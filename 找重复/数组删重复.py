# -*- coding: utf-8 -*-


def remove_element(nums, val):
    """
    https://leetcode.com/problems/remove-element/description/
    把所有等于val的值，放到输入数组的后边，然后输出最新的数组的长度
    双指针 i 和 j，开始的时候分别指向第一个和最后一个元素，挪动i和j，找到val的时候挪动j
    """
    if nums:
        i, j = 0, len(nums) - 1
        while i <= j:
            if nums[i] == val:
                # 找到了i = val的时刻，挪动j
                while j >= i and nums[j] == val:
                    j -= 1
                if j >= i:
                    nums[i] = nums[j]
                    j -= 1
            i += 1
        return j + 1
    return 0

