# -*- coding: utf-8 -*-
from collections import deque


class GNode(object):
    def __init__(self, key):
        self.key = key
        self.adj = list([])
        self.inDegree = 0
        self.visitStatus = "NOT YET"

    def __repr__(self):
        return "key={} {} in degree={}".format(self.key, self.visitStatus, self.inDegree)

    def addPrereq(self, pr):
        pr.adj.append(self)
        self.inDegree += 1


def canFinish(prereq):
    def dfsCheckNoCycle(graph, course_id):
        courseNode = graph[course_id]
        if courseNode.visitStatus == "VISITING":
            # find a cycle if visiting this node already
            return False
        if courseNode.visitStatus == "VISITED":
            return True
        courseNode.visitStatus = "VISITING"
        for adjCourseNode in courseNode.adj:
            if not dfsCheckNoCycle(graph, adjCourseNode.key):
                return False
        courseNode.visitStatus = "VISITED"
        return True

    # first create a graph dict
    graph, courseIDs = {}, set([])
    for c1, c2 in prereq:
        courseIDs.add(c1)
        courseIDs.add(c2)
        if c1 not in graph: graph[c1] = GNode(c1)
        if c2 not in graph: graph[c2] = GNode(c2)
        graph[c1].adj.append(graph[c2])

    for i in courseIDs:
        if not dfsCheckNoCycle(graph, i):
            return False
    return True


def test1():
    data = [
        (2, [[1, 0]]),
        (2, [[1, 0],[0,1]]),
        (3, [[1, 0], [2, 0], [1, 2]]),
        (4, [[1, 0], [2, 0], [1, 2], [3, 1]]),
        (4, [[1, 0], [2, 0], [1, 2], [3, 1], [0, 3]])
        ]
    for _, preq in data:
        print canFinish(preq)


def finishOrder(n, prereq):
    # generate graph
    # 这里需要把所有的node都创建，因为最后是一个order，必然包含所有的course
    graph = {i: GNode(i) for i in xrange(n)}
    for c1, c2 in prereq:
        # graph[c1].addPrereq(graph[c2])
        graph[c2].adj.append(graph[c1])
        graph[c1].inDegree += 1
    # find nodes with 0 in degree
    zero_indegree_queue = deque([])
    for node in graph.values():
        if node.inDegree == 0:
            zero_indegree_queue.append(node)

    order = []
    while zero_indegree_queue:
        courseNode = zero_indegree_queue.popleft()
        for adjCourse in courseNode.adj:
            adjCourse.inDegree -= 1
            if adjCourse.inDegree == 0:
                zero_indegree_queue.append(adjCourse)
        order.append(courseNode.key)
    return order if n == len(order) else []


def test2():
    data = [
        (10, []),
        (2, [[1, 0]]),
        (2, [[1, 0],[0,1]]),
        (3, [[1, 0], [2, 0], [1, 2]]),
        (4, [[1, 0], [2, 0], [1, 2], [3, 1]]),
        (4, [[1, 0], [2, 0], [1, 2], [3, 1], [0, 3]]),
        (4, [[1, 0], [1, 3], [3, 2], [2, 1]])
        ]
    for n, preq in data:
        print finishOrder(n, preq)


test2()