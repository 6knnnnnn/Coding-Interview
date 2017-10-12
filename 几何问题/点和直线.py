# -*- coding: utf-8 -*-

"""
y = kx + b
两个问题：如何创建+表示不同的line，以及如何判断某个point是否在line上边
当k=无穷，此时直线和y轴平行（和x轴垂直），此时判断point是否在这个线上，只要判断point.x是否等于line.x
当k=0，此时直线和x轴平行（和y轴垂直），即y=b，此时判断point是否在这个线上，只要判断point.y是否等于line.b
其他情况，根据k和b计算出point.y = point.x * k + b。所以k=0的line和此时的line判断依据均为y = kx + b，既不需要override
"""


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class LineRegular(object):

    def __init__(self, k, b):
        self.k = k
        self.b = b
        self.point_count = 0

    def add_point(self):
        self.point_count += 1

    def __str__(self):
        return "{}%{}".format(self.k, self.b)

    def is_point_in_line(self, point):
        return point.y == self.k * point.x + self.b

    @staticmethod
    def build_new_line(A, B):
        if A.x == B.x:
            return LineVertical(A.x)
        else:
            # 默认k b为与x轴平行的情况
            k, b = 0.0, float(A.y)
            if A.y != B.y:
                k = float(abs(A.y - B.y)) / float(abs(A.x / B.x))
                b = A.y - k*A.x
            return LineRegular(k, b)


class LineVertical(LineRegular):
    def __init__(self, x):
        LineRegular.__init__(self, k=None, b=None)
        self.x = x

    def is_point_in_line(self, point):
        # 覆盖父类的判断方法
        return point.x == self.x

    def __str__(self):
        return "None:{}".format(self.x)


def max_points_on_a_line(points):
    """
    https://leetcode.com/problems/max-points-on-a-line/
    第一次扫，两次loop，创建所有可能的line，存到一个map里面，key为k%b，这样避免重复创建Line object
    LineRegular的key为k%b，LineVertical的key为"None:x"
    第二次扫，根据所有点，和所有可能的line，如果点属于line，更新line point count，同时更新含有最多点的line的个数
    如果是包含最多点的line，需要第二次扫更新max point的同时，更新max point line
    时间复杂度O(N^2)
    """
    line_table = dict([])
    for i in xrange(len(points)-1):
        for j in xrange(i+1, len(points)):
            line = LineRegular.build_new_line(points[i], points[j])
            if str(line) not in line_table:
                line_table[str(line)] = line
    max_point = 0
    for point in points:
        for line in line_table.values():
            if line.is_point_in_line(point):
                line.add_point()
                max_point = max(max_point, line.point_count)

    return max_point


def skyline(buildings):
    """
    https://leetcode.com/problems/the-skyline-problem/description/
    """
