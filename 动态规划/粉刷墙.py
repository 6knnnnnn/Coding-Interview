# -*- coding: utf-8 -*-

import sys


def paint_fence(n, k):
    """
    https://leetcode.com/problems/paint-fence/description/
    有N个fence，K种颜色，每次最多有两个相邻fence是同一个颜色，求最后有多少种喷漆的方式。
    如果N = 0，返回0，如果N = 1，只有K种可能，不存在diff的情况
    如果N = 2，第一个fence有K种可能，第二个fence要看情况：如果跟1相同，K*1种可能，否则，K*(K-1)种可能
    所以对于N >= 3，以此类推，根据上一个fence涂颜色的可能性same and diff，对于本次来说：
        same_current = total_previous
        diff_current = total_previous * (k - 1)
        total_current = same_current + diff_current
    """
    if n == 0:
        return 0
    if n == 1:
        return k
    same_prev, diff_prev = k, k*(k-1)
    for i in xrange(3, n+1):
        same_curr = total_prev = same_prev + diff_prev
        diff_curr = total_prev * (k-1)
        same_prev, diff_prev = same_curr, diff_curr
    return same_prev + diff_prev


def paint_house(costs):
    """
    https://leetcode.com/problems/paint-house/description/
    有红绿蓝三种颜色的油漆，用来粉刷连成了一排的N个房子，每个房子的每个颜色成本不一样，用一个N*3的矩阵表示。
    找到一种粉刷房子的方法，使得最后的粉刷成本为最低，而且相邻的房子的颜色不能一样。
    解法：时间O(N)，空间O(1)
        每次粉刷房子，根据前一个房子的颜色，有两种选择，即排除掉之前房子颜色的其他两种。
        那么需要有三个变量，分别记录从开始到目前的房子，分别用3种颜色后，对应的油漆成本。
        即递推公式为：当前房子图上颜色R的累加成本 = 当前房子R颜色的成本 + min(之前房子图上G或者B颜色的累加成本)
        最后返回d的是三者中最小的cost
    """
    # accumulative cost of color Red/Green/Blue so far
    accuR, accuG, accuB = 0, 0, 0
    for c in costs:
        # Current cost depends on previous costs; each c is an array of size 3
        curR = c[0] + min(accuB, accuG)
        curG = c[1] + min(accuR, accuB)
        curB = c[2] + min(accuR, accuG)
        accuR, accuG, accuB = curR, curG, curB
    return min(accuR, min(accuG, accuB))


def paint_house_k_colors(hc_costs):
    """
    https://leetcode.com/problems/paint-house-ii/description/
    类似于上边的题目，只不过这里面有K种颜色，需要找到对应的所有N个房子的刷油漆的最小成本。

    对于每一个house，如果每次都是找到对于颜色x，之前的最小涂色的成本，会非常耗时。
    其实这个时候我们只关心有限个变量：
        1. 之前一次的house选择的颜色是什么，prev_house_color_index，以及对应的最小成本prev_house_cost_min
        2. 当前house的index，对于它的每一个color cost 以及其中最小的color cost index
        3. 如果这个 color index = prev_house_color_index，即跟前一次house的最小颜色的index一样，我们不能选择当前color
           而是要选择第二小的color（肯定和当前的color index不一样）
        4. 所以，除了prev_house_cost_min，还需要记录第二小的prev_house_cost_min2
    即每次我们根据前一个house所知道的最小和第二小的color cost，以及前一个house的color index，来找到当前house的 min color cost

    所以在找不同颜色的最小值不是遍历所有不同颜色，而是用min1和min2来记录之前房子的最小和第二小的花费的颜色
    如果当前房子颜色和min1相同，那么我们用min2对应的值计算，反之我们用min1对应的值。

    这道题目有点类似买卖股票，即需要知道当前price之前的min price。
    可能的follow up，找到最好的方案，即path，需要一个单独的list，来记录每次每个house对应的color是什么。
    """
    if not hc_costs or not hc_costs[0]:
        return 0
    # 最开始的时候，两个min都是0 - dp[0] 初始化条件
    min1 = min2 = 0
    prev_house_color_idx = -1
    # costs = N*K 矩阵
    # DP[i] -> 当前house i，成本最小的color index + cost (min1)，成本第二小的 cost (min2)
    for house_color_cost in hc_costs:
        curr_min1 = curr_min2 = sys.maxint
        curr_house_color_idx = -1
        for color_idx, color_cost in enumerate(house_color_cost):
            # 如果当前color index和上一次的house color index相同，需要选择min2
            color_cost += min2 if color_idx == prev_house_color_idx else min1
            if color_cost < curr_min1:
                # curr_house_color_cost < curr_min1 < curr_min2, swap 1, 2 with new, 1
                curr_min2, curr_min1 = curr_min1, color_cost
                curr_house_color_idx = color_idx
            elif color_cost < curr_min2:
                # curr_min1 < color_cost < curr_min2, swap 2 with new
                curr_min2 = color_cost
        min1, min2, prev_house_color_idx = curr_min1, curr_min2, curr_house_color_idx
    return min1
