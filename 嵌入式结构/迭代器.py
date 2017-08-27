# -*- coding: utf-8 -*-
from collections import deque


# https://leetcode.com/problems/flatten-nested-list-iterator/description/
class NestedIteratorDFS(object):
    """
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