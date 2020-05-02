# -*- coding: utf-8 -*-
"""
给定一个非常大的文件，里面每一行是一个integer，要求找到这些整数的median。

如果我们知道了总共有多少行integer，那么就等价于，排序所有整数，然后找到中间位置的integer即可。

总行数 = total，中位数位置index需要根据total是奇数还是偶数来判断：如果是偶数还需要求品均。

因为文件很大无法读入到内存中，需要做特殊处理：做range search

大意就是，每次根据upper and lower bound  计算出来一个平均值x，用来猜数字

然后扫一遍整个的文件，找到小于这个x的数量为count：
如果count == index，就是需要找的值，返回x
如果count > index，说明需要把 x + 1 当做是新的upper，然后去左边找，从新扫描一遍
如果count < index，说明需要把 x 当做是新的lower，然后去右边找，从新扫描一遍

时间复杂度取决于integer的值域，如果是32位的，那么最多需要扫描整个文件32次，即二分法，所以是O(32*N)

暴力解法：对于每一个数字，找到有多少个数字小于他，时间O(N^2)。
"""
import sys


def search(nums, index, lower, upper):
    if lower == upper:
        return lower
    candidate = lower
    x = (lower + upper) >> 1
    count = 0
    for n in nums:
        if n <= x:
            count += 1
            # 此时需要更新candidate，即需要找到最接近x的数值
            candidate = max(candidate, n)
    if count == index:
        return candidate
    elif count < index:
        # candidate 肯定小于 x，但是如果candidate+1比x大，
        # candidate + 1 才是真正的新的upper bound
        return search(nums, index, max(x, candidate+1), upper)
    else:
        # candidate 肯定小于 x，所以candidate才是真正的新的upper bound
        return search(nums, index, lower, candidate)


def find_median(nums):
    total = 0
    for _ in nums:
        total += 1
    if total % 2 == 1:
        return search(nums, total/2 + 1, -sys.maxint, sys.maxint)
    else:
        left  = search(nums, total/2, -sys.maxint, sys.maxint)
        right = search(nums, total/2 + 1, -sys.maxint, sys.maxint)
        # 算出来平均数
        return (left + right) >> 2
