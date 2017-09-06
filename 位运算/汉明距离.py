# -*- coding: utf-8 -*-


def hamming_weight(x):
    # 返回一个数字的汉明权重，即binary string中，所包含1的个数
    total = 0
    while x:
        total += x & 1
        x >>= 1
    return total


def hamming_distance(x, y):
    """
    https://leetcode.com/problems/hamming-distance/description/
    两个数字的汉明距离，即两个数的bit中，相同位bit数字不同的总数。
    1   (0 0 0 1)
    4   (0 1 0 0)
    1 和 4 的汉明距离为2，即2位不同。
    最简单的做法，将x^y的结果变为binary string，然后找到1的数量。
    """
    total = 0
    while x or y:
        # 分别找到x y的最后一位，取异或，加到total里面，然后右移x y
        total += (x & 1) ^ (y & 1)
        x, y = x >> 1, y >> 1
    return total


def total_hamming_distance(nums):
    """
    https://leetcode.com/problems/total-hamming-distance/description/
    找到所有数字中，两两之间的汉明距离。
    解法1：暴力双层for loop，调用API找到两个数之间的距离，时间O(N^2)
    解法2：按照column来处理所有输入，找到每一个数字对应column上边，0和1的数量分别为x y，那么这一个column上边所有的可能组合为
    x * y，即最后的结果需要加上这个x * y。时间复杂度O(NlogM)，M为数字的值域（logM即总共的column数量）。
    """
    total = 0
    if nums:
        # 找到最大的数字，以及对应的binary string长度
        max_length = len(bin(max(nums))) - 2
        for i in xrange(max_length):
            # x1 x0 分别记录1和0的数量
            x1 = x0 = 0
            for n in nums:
                # 左移i位，跟1取AND，即为第i位的bit数字
                if (n >> i) & 1:
                    x1 += 1
                else:
                    x0 += 1
            total += x1 * x0
    return total
