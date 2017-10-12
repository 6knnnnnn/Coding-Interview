# -*- coding: utf-8 -*-

"""
从n个数中，找到k个数字，组合的可能性以及排列的可能性分别为
Cnk = n! / ( k! * (n-k)! )
Pnk = n! / (n-k)!
如果 k = n，即从n个数字中找n中可能的排列，总共有n!种方式
"""


def permutation_distinct(nums):
    """
    https://leetcode.com/problems/permutations/description/
    给定一个数组里面不包含任何重复，返回其中的所有可能的排列情况
    需要三重for loop
    如果nums里面没有任何元素，即0! = 1，返回一种结果，即[[]]
    对于nums里面的每一个元素n，对于已经存在于res的排列，即从第1个到n-1的排列，把n插入到每个排列的每一个位置上去
    """
    all_perm = [[]] # 0！= 1 的结果
    for n in nums:
        # 根据已有的res，来创建出当前的permutation，然后代替已有的res
        curr_perm = []
        for exist_perm in all_perm:
            for i in xrange(len(exist_perm)+1):
                # 分别把n插入到prev_perm的每一个位置上去，即 left + n + right
                # i需要访问到len(exist_perm)，因为到最后一个元素的时候，n要插入到最后 [...] + [n] + []
                new_perm = exist_perm[:i] + [n] + exist_perm[i:]
                curr_perm.append(new_perm)
        all_perm = curr_perm
    return all_perm


def permutation_duplicated(nums):
    """
    https://leetcode.com/problems/permutations-ii/description/
    给定数组里面包括重复的数字，返回所有可能的排列，但必须没有重复的
    关键点：如果将某个数字k加入到某一个排列中 [ ...j, k, k, l...]，那么连续的k只需要插进去一次就好
    即[ ...j, k, k, k, l...]，之后跳过这段连续的k，继续到l
    """
    all_perm = [[]]
    for n in nums:
        # 根据已有的res，来创建出当前的permutation，然后代替已有的res
        curr_perm = []
        for prev_perm in all_perm:
            for i in xrange(len(prev_perm)+1):
                # 分别把n插入到prev_perm的每一个位置上去，即 left + n + right
                # i需要访问到len(prev_perm)，因为到最后一个元素的时候，n要插入到最后 [...] + [n] + []
                new_perm = prev_perm[:i] + [n] + prev_perm[i:]
                curr_perm.append(new_perm)
                if i < len(prev_perm) and prev_perm[i] == n:
                    # 此时代表有重复的，那么跳过prev_perm[i]之后的元素
                    break
        all_perm = curr_perm
    return all_perm


def next_higher_permutation(nums):
    """
    https://leetcode.com/problems/next-permutation/description/
    给定一个数组，代表的是一个整数，每个元素代表每一位，要求根据这个整数，找到所有数字的排列组合当中
    刚好比当前数字大的下一个数字的数组表示，如果没有更大的，返回最小的排列组合。
    """
    def reverse(nums, start, end):
        # swap an array/list from start to end
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    if len(nums) >= 2:
        i = len(nums) - 1
        while i > 0 and nums[i] > nums[i - 1]:
            # 从后往前找到一段满足逆序排序的子数组区间
            i -= 1
        # 此时nums[i-1...n-1] 是逆序排序的
        if i == 0:
            # the whole nums in reverse order, swap all
            reverse(nums, 0, len(nums) - 1)
        else:
            # left=nums[0...i], right=nums[i-1...n-1]
            j = len(nums) - 1
            while j >= i and nums[j] > nums[i - 1]:
                # find the smallest in right that bigger than nums[i]
                j -= 1
            nums[j], nums[i - 1] = nums[i - 1], nums[j]  # swap
            # now nums[i-1...n-1] still in reverse order
            reverse(nums, i, len(nums) - 1)


def previous_lower_permutation(s):
    """
    https://leetcode.com/problems/previous-permutation/description/
    :param s:
    :return:
    """


def palindrome_permutation_generate(s):
    """
    https://leetcode.com/problems/palindrome-permutation-ii/description/
    给定一个string，返回所有可能的回文排列，如果有的话。
    本质上是排列组合问题，但此时我们只需要排列"一半"的字母即可，即那些出现次数为偶数个的字母
    因为回文要求就是，左半边和右半边完全相等
    """
