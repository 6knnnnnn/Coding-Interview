# -*- coding: utf-8 -*-


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
    有红绿蓝三种颜色的油漆，用来粉刷连成了一排的N个房子，每个房子的颜色成本不一样，用一个N*3的矩阵表示。
    找到一种粉刷房子的方法，使得最后的粉刷成本为最低，而且相邻的房子的颜色不能一样。
    解法：时间O(N)，空间O(1)
        每次粉刷房子，根据前一个房子的颜色，有两种选择，即抛出之前房子的颜色的其他两种。
        那么需要有三个变量，分别记录从开始到目前的房子，分别用3种颜色后，对应的油漆成本。
        即递推公式为：当前房子图上颜色R的累加成本 = 当前房子R颜色的成本 + min(之前房子图上G或者B颜色的累加成本)
        最后返回d的是三者中最小的cost
    """
    accuR, accuG, accuB = 0, 0, 0
    for c in costs:
        # Current cost depends on previous costs
        curR = c[0] + min(accuB, accuG)
        curG = c[1] + min(accuR, accuB)
        curB = c[2] + min(accuR, accuG)
        accuR, accuG, accuB = curR, curG, curB
    return min(accuR, min(accuG, accuB))


def paint_house_k_colors(costs):
    """

    :param costs:
    :return:
    """

