# -*- coding: utf-8 -*-


def valid_square(p1, p2, p3, p4):
    # https://leetcode.com/problems/valid-square/description/
    # 给定四个点的坐标，判断四个点是否能组成一个正方形，四条边长度相等，两条对边平行，相邻边垂直
    # 但问题是需要知道每两个点，是处在对角线，还是相邻边上，实现起来会很麻烦
    # 所以其实可以看所有点和点之间的距离，对角线的距离有2个，相邻边的距离有4个，正方形必须满足这些
    def get_distance(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    points = [p1, p2, p3, p4]
    distance_count = dict([])
    for i in xrange(4):
        for j in xrange(i+1, 4):
            dist = get_distance(points[i], points[j])
            distance_count[dist] = distance_count.get(dist, 0)+1
    key_set, value_set = distance_count.keys(), distance_count.values()
    return len(key_set) == 2 and 2 in value_set and 4 in value_set


def maximum_square(matrix):
    """
    https://leetcode.com/problems/maximal-square/description/
    找到一个只包含01的矩阵中，能够形成的最大的正方形面积，比如下图，面积为4
    1 0 1 0 0
    1 0 1 1 1
    1 1 1 1 1
    1 0 0 1 0
    解法和Maximal Rectangle那道题目类似，都是以某一行
    """