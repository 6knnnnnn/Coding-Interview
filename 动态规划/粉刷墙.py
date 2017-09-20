# -*- coding: utf-8 -*-


def paint_fence(n, k):
    """
    https://leetcode.com/problems/paint-fence/description/
    有N个fence，K种颜色，每次最多有两个相邻fence是同一个颜色，求最后有多少种喷漆的方式。
    """


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

