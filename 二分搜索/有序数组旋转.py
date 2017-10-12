# -*- coding: utf-8 -*-

"""
http://bangbingsyb.blogspot.com/2014/11/leetcode-search-in-rotated-sorted-array.html

问题关键点，对于数组，找到start mid end三个index，判断哪一部分是排好序的
1. 如果刚好target = mid，返回mid即可
2. 否则如果target刚好在排序的那一部分，那肯定要去那一部分，否则只能去往另一部分。

原数组： 0 1 2 4 5 6 7

其实这里面所谓的rotate left or right，是说对于中间点mid，到底是左边顺序被打乱了，还是右边顺序被打乱了
如果没有rotate，肯定满足 start < mid < end （假设没有重复）。
如果有，根据左右两部分，哪一边的更多的元素挪到了另一边，可能有两种情况：

情况1：  6 7 0 1 2 4 5 rotate 左边，更多的元素从左边挪到了右边
    起始元素0在中间元素1的左边，mid 到 end 是排序的，而且 mid 1 < end 5 < start 6
        如果 mid < target <= end，去右边，否则如果 target < mid，去左边

    Edge case 假设 2 4， 即只有2个元素，刚开始 mid = start = 2 < end = 4
        如果 mid < target <= end 那肯定是去右边，比如target = 4
        否则，判断 mid 是否等于 target，比如target = 1 or 2

情况2：  2 4 5 6 7 0 1 rotate 右边，更多的元素从右边挪到了左边
    起始元素0在中间元素6的右边，start 到 mid 是排序的，而且 mid 6 > start 2 > end 1
        如果 start <= target < mid，去左边，否则如果 target > mid，去右边

    Edge case 假设 4 2，刚开始 mid = start = 4 > end = 2
        如果 start <= target < mid 左半序列，否则右半序列

所以结合edge case，我们需要通过 mid 和 end的关系来判断是左边还是右边。
（mid和start的关系不确定，如果是edge case 即只有两个元素 那么 mid = (start+end) / 2 == start）
"""


def search_in_rotated_sorted_array(nums, target):
    """
    https://leetcode.com/problems/search-in-rotated-sorted-array/description/
    某个原本排序的数组被旋转了一次，给定一个数字，找到这个数组中是否存在以及对应的index，不存在则返回-1
    """
    if nums:
        i, j = 0, len(nums) - 1
        while i <= j:
            m = (i + j) >> 1
            start, mid, end = nums[i], nums[m], nums[j]
            if mid == target:
                return m
            if mid < end:
                # 情况1，mid end 是排好序的，即右边
                if mid < target <= end:
                    # target在右边，更新i
                    i = m + 1
                else:
                    j = m - 1
            else:
                # 情况2，start mid 是排好序的，即左边
                if start <= target < mid:
                    j = m - 1
                else:
                    i = m + 1
    return -1


def search_in_rotated_sorted_array_duplicates(nums, target):
    """
    https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/
    此时如果有重复，会出现 mid == end 的情况。此时右半序列可能是sorted，也可能并没有sorted，如下例子：

    没排序 3 1 2 3 3 3 3
    排序了 3 3 3 3 1 2 3
    如果找1，不知道往哪里走

    所以当 mid = end != target时，无法排除一半的序列，而只能排除掉A[end]，需要继续搜寻A[start : end-1]
    正因为这个变化，在最坏情况下，算法的复杂度退化成了O(n)：比如 2 2 2 2 2 2 2 中寻找target = 1。
    """
    if nums:
        i, j = 0, len(nums) - 1
        while i <= j:
            m = (i + j) >> 1
            start, mid, end = nums[i], nums[m], nums[j]
            if mid == target:
                return m
            if mid < end:
                # 情况1，mid end 是排好序的，即右边
                if mid < target <= end:
                    # target在右边，更新i
                    i = m + 1
                else:
                    j = m - 1
            elif mid > end:
                # 情况2，start mid 是排好序的，即左边
                if start <= target < mid:
                    j = m - 1
                else:
                    i = m + 1
            else:
                # 出现了重复 mid == end，缩短end-1
                j -= 1
    return -1


def find_minimum_in_rotated_sorted_array(nums):
    """
    http://bangbingsyb.blogspot.com/2014/11/leecode-find-minimum-in-rotated-sorted.html
    https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/
    找到旋转数组中最小值，此时假设没有重复。如果没有旋转，最小值就是nums[0]
    如果rotate左边，即情况1，最小值在左边，否则rotate右边，即情况2，最小值在右边。

    和Search in Rotated Sorted Array I这题换汤不换药。同样可以根据A[mid]和A[end]来判断右半数组是否sorted：

    原数组：0 1 2 4 5 6 7

    情况1：  6 7 0 1 2 4 5
    mid < end  从 mid 到 end 是排好序的，min不在 [mid+1 : end]中，搜索 [start : mid]

    情况2：  2 4 5 6 7 0 1
    mid > end [start : mid] sorted，且又因为该情况下 end < start，min不在 [start : mid]中，搜索 [mid+1 : end]

    Edge case
    a. start =  end，必然 start 为min，为搜寻结束条件。
    b. start + 1 = end，此时 mid =  start，而在情况1和2中
    每次如果有 mid < end就去左边，左边也就是start/mid自己，所以已经处理了这种情况
    """
    if nums:
        i, j = 0, len(nums) - 1
        while i < j:
            m = (i + j) >> 1
            if nums[m] < nums[j]:
                # rotate左边，min在左边，情况1，第一个元素在左边
                j = m
            else:
                i = m + 1
        return nums[i]
    return None


def find_minimum_in_rotated_sorted_array_duplicates(nums):
    """
    https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/description/
    和Search in Rotated Sorted Array II这题换汤不换药。同样当A[mid] = A[end]时，无法判断min究竟在左边还是右边。

    3 1 2 3 3 3 3
    3 3 3 3 1 2 3

    但可以肯定的是可以排除A[end]：因为即使min = A[end]，由于A[end] = A[mid]，排除A[end]并没有让min丢失。所以增加的条件是：

    A[mid] = A[end]：搜索A[start : end-1]
    """
    if nums:
        i, j = 0, len(nums) - 1
        while i < j:
            m = (i + j) >> 1
            if nums[m] < nums[j]:
                # rotate左边，min在左边，情况1，第一个元素在左边
                j = m
            elif nums[m] > nums[j]:
                i = m + 1
            else:
                j -= 1
        return nums[i]
    return None
