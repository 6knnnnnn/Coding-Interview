# -*- coding: utf-8 -*-


def container_with_most_water(heights):
    """
    https://leetcode.com/problems/container-with-most-water/description/
    给定一个array，里面都是柱子的高度，找到灌水最多的两个柱子组合。
    左右边界的双指针，每次计算出以(r-l)为底， min(heights[l], heights[r])为高度的container的水容积
    高度小的一方，pointer向中间移动。比如，如果左边的指针的高度小于右边的，向左边移动l+1。
    1 3 1 2 4 2
            |
      |     |
      |   | | |
    | | | | | |
    -----------
    0 1 2 3 4 5
    l=0 r=5 -> l=1 r=5 -> l=1 r=4 -> l=2 r=4 -> l=3 r=4
    """
    l, r = 0, len(heights) - 1
    max_vol = 0
    while l < r:
        new_vol = (r - l) * min(heights[l], heights[r])
        max_vol = max(max_vol, new_vol)
        if heights[l] < heights[r]:
            l += 1
        else:
            r -= 1
    return max_vol


def trap_rain_water(h):
    """
    https://leetcode.com/problems/trapping-rain-water/description/
    http://fisherlei.blogspot.com/2013/01/leetcode-trapping-rain-water.html
    如果把直方图当做是蓄水池，求问下雨后，总共的能够盛水的面积（容积）？

    Follow up可能是：哪一部分的蓄水池能够存放最多的雨水。

    解法1：类似于直方图最大矩阵面积，不过此时需要求矩阵的最小值，也就是能够成水的最大值。
    所以要用一个单调递减stack，以及在更新的时候

    解法2：DP + 扫描
    对于每一个bar来说，能装水的容量取决于左右两侧bar的最大值，两者中较小的一个bar，才是木桶效应的"短板"。
    从左向右，记录对于每个bar 左侧的最大高度left[i]，从右向左，记录每个bar右侧的最大高度right[i]
    第三次扫描，则对于每一个bar，计算
        （1）左侧最大height和当前bar的height的差值（left[i] - heights[i]）
        （2）右侧最大height和当前bar的height的差值（right[i] - heights[i]）
        取（1），（2）中结果小的那个作为当前bar的蓄水量。最终求和得到总蓄水量。
    """
    l = total = max_left = max_right = 0
    r = len(h) - 1
    while l <= r:
        max_left = max(max_left, h[l])
        max_right = max(max_right, h[r])
        if max_left < max_right:
            total += max_left - h[l]
            l += 1
        else:
            total += max_right - h[r]
            r -= 1
    return total
