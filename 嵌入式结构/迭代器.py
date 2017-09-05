# -*- coding: utf-8 -*-
from collections import deque


class NestedIteratorDFS(object):
    """
    https://leetcode.com/problems/flatten-nested-list-iterator/description/
    DFS的做法就是，用一个deque，初始化的时候，把所有的元素放到deque里面
    但是这样并不是真的迭代器，其实等价与用一个额外空间来存放整体的元素，而非一个一个的迭代
    """
    def __init__(self, nested_obj_list):
        self.queue = deque([])
        for elem in nested_obj_list:
            if elem.isInteger():
                self.queue.append(elem.getInteger())
            else:
                # DFS 生成一个新的iterator，然后把所有元素放到queue里面
                nested_list_iterator = NestedIteratorDFS(elem.getList())
                while nested_list_iterator.has_next():
                    self.queue.append(nested_list_iterator.next())

    def has_next(self):
        return len(self.queue) > 0

    def next(self):
        return self.queue.popleft()


class NestedIteratorBFS(object):
    """
    BFS用stack，每一个元素为nested object，和对应的index
    如果下一个next出来的元素是一个list，把list里面
    """
    def __init__(self):
        pass

    def next(self):
        pass

    def has_next(self):
        pass


class Flatten2DVector(object):
    """
    https://leetcode.com/problems/flatten-2d-vector/description/
    为一个2D数组设计一个iterator
    """
    def __init__(self, vec2d):
        self.row = self.col = 0
        self.vec = vec2d
        self.total_row = len(self.vec)

    def next(self):
        if self.row >= self.total_row:
            # row越界了
            raise Exception("No more element")
        if self.col >= len(self.vec[self.row])-1:
            # 对于当前合法row，col越界了，那么需要找到下一个合法的row的第一个col
            if self.row == self.total_row - 1:
                raise Exception("No more element")
            self.col, self.row = 0, self.row + 1
            while self.row < self.total_row and len(self.vec[self.row]) == 0:
                self.row += 1
            if self.row == self.total_row:
                raise Exception("No more element")
        else:
            # 对于当前合法row，col还没有越界
            self.col += 1
        return self.vec[self.row][self.col]

    def hasNext(self):
        return self.row < self.total_row and self.col < len(self.vec[self.row])
