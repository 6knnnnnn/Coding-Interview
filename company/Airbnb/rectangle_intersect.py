# -*- coding: utf-8 -*-
"""
给定一个数组里面全是point，[[a, b], [c, d]] a b是一个矩形的左下角的坐标，c d是这个矩形的右上方坐标

找到他们当中有overlap的个数。

follow up：有哪些有overlap？即哪些是同一"组"的？需要根据parent link array里面的index来判断
"""
from collections import defaultdict


def is_overlap(points1, points2):
    # 如果overlap面积为0，即没有overlap
    A, B = points1[0]
    C, D = points1[1]
    E, F = points2[0]
    G, H = points2[1]
    x = max(min(C, G) - max(A, E), 0)
    y = max(min(D, H) - max(B, F), 0)
    return x * y != 0


def find(i, parents_link):
    # 给定一个parent link array，找到i的对应parent是哪一个
    while parents_link[i] != i:
        i = parents_link[i]
    return i


def find_intersection(rectangles):
    """
    例子：矩形0-7，013有交集，246有交集，5和7分别是独立的
    那么parent link初始化为 [0, 1, 2, 3, 4, 5, 6, 7]
    之后双层循环遍历矩形 [0, 1, 2, 3, 4, 5, 6, 7]
    0：[3, 1, 2, 3, 4, 5, 6, 7]，即0先是变为1，然后变为3（后来居上）
    1：[3, 3, 2, 3, 4, 5, 6, 7]，即1变为3（3在1后边，跟1有交集，所以3成为了1的parent）
    2：[3, 3, 6, 3, 4, 5, 6, 7]，即2先是变为4，然后变为6
    3：[3, 3, 6, 3, 4, 5, 6, 7]，没有变没有交集
    4：[3, 3, 6, 3, 6, 5, 6, 7]，即4变成了6
    5：[3, 3, 6, 3, 6, 5, 6, 7]，没有交集没有变
    6：[3, 3, 6, 3, 6, 5, 6, 7]，没有变没有交集
    7：[3, 3, 6, 3, 6, 5, 6, 7]，没有变没有交集

    所以最后根据[3, 3, 6, 3, 6, 5, 6, 7]，我们可以有 parent-child-pair
    3: [0, 1, 3], 6: [2, 4, 6], 5: [5], 7: [7]
    """
    # initialize parents link array with its own index
    parents_link = range(len(rectangles))
    for i in xrange(len(rectangles)-1):
        for j in xrange(i+1, len(rectangles)):
            # 矩形两两相比较
            r1, r2 = rectangles[i], rectangles[j]
            if is_overlap(r1, r2):
                root1 = find(i, parents_link)
                root2 = find(j, parents_link)
                # 因为是两层循环，最开始的矩形的parent是后边的跟它相交的矩形
                if root1 != root2:
                    parents_link[root1] = root2
    group = defaultdict(list)
    for i in parents_link:
        root = parents_link[i]
        group[root].append(i)
    # 最后返回的是一个list，里面每个元素是一个list，存放的是所有互相有overlap矩形的index
    return group.values()
