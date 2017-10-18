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
    https://segmentfault.com/a/1190000003786782
    给定一个数组，包含了一个建筑物的left, right and height，即在二维空间中的坐标
    返回一个数组，里面每个元素是一个点，要求如果根据这些点来画坐标的图形，应该得到的是overlapping之后的skyline

    先把所有的点parse成(x, y, start|end)，x横坐标，y纵坐标height，start|end状态，按x/y坐标排序（相同x，y小的排在前面）
    同时，维持一个max heap，初始化为只有0，root是当前图形的所有顶点中最高的点（相同的max可能有多个）
    每次更新（插入或删除）heap后，判断之前的root是否被改变，只要这个root没变（即max值没变），说明这个最高的矩形还没结束

    遍历所有的点，每次遍历根据x, y, start|end判断：
        当遇到一个start，把y进入到PQ中去（即便有重复的值也没关系，关心的是最高点，不关心有几个，重复的高度最后都需要merge）
        当遇到一个end，意味着以这个点为结束点的矩形需要结束了，此时根据height y，找到heap中对应的start point，把它从heap中删掉
        此时如果这个点的height，大于删除后max heap root，说明我们找到了一个新的高度（变矮了，需要"向下"转折），需要加入到output

    空间O(N)用来构建点，以及heap size；时间这里分为步骤1) parse+sort NlogN 2) insert to heap logN  3) delete heap N
    2和3是在遍历N个元素的时候进行的，所以总的时间复杂度为O(NlogN + N^2)
    如果有类似于TreeMap的数据结构，里面都是排序的，每次insert和delete都是logN，那么最后的时间复杂度为O(NlogN)
    """



