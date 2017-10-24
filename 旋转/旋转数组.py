# -*- coding: utf-8 -*-


def swap(array, start, end):
    if start < len(array) and end < len(array):
        while start < end:
            array[start], array[end] = array[end], array[start]
            start, end = start + 1, end - 1


def rotate_array_3_times(nums, k):
    """
    https://leetcode.com/problems/rotate-array/description/
    swap 3次，第一次全部，第二次0到k-1，第三次k到len(nums)-1
    所以总共O(2 * N)次
    """
    swap(nums, 0, len(nums)-1)
    swap(nums, 0, k-1)
    swap(nums, k, len(nums)-1)


def rotate_array_left_right(nums, k):
    """
    以K为分割点，比较数组中左部分和右部分的长度left right（K属于左边），谁小先换谁且换完后固定，然后处理中间之后的。
    如果left>right：abc d | efg -> efg | d abc -> ef | abc d
        把左边的前right个字符和右边的所有right个字符互换（right换left的前缀）
        对于没有换的中间部分，把他们跟换完之后的最后的right个字符依次互换
        这样子，中间的部分和right部分只换了总长度的1/2次
    同理如果right>left：ab | cd ef -> ef | cd ab -> ef | ab  cd
        把左边的所有left个字符跟右边的从后往前数left个字符交换（left换右边的后缀）
        对于没有换的中间部分，把他们跟换完之后的前边的left个字符依次互换
        这样子，中间的部分和left部分只换了总长度的1/2次
    最好的情况，如果left = right，那就对半rotate，此时所有的元素我们只需要遍历N/2次就能完成交换了。
    """
    pass


def rotate_list(head):
    pass


def move_zeroes(nums):
    """https://leetcode.com/problems/move-zeroes
    把所有的0挪到数组末尾，但不改变其它非0数字的顺序
    两个指针，i负责指向当前非0元素，j指向某一段连续0元素的最后一个0，之后swap
    """
    i = j = 0
    while i < len(nums) and j < len(nums):
        while nums[j] == 0:
            j += 1
            if j == len(nums):
                return
        nums[i], nums[j] = nums[j], nums[i]
        i, j = i+1, j+1
    return nums

