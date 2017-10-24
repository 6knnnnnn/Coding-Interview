# -*- coding: utf-8 -*-
from collections import deque


class FlattenNestedIteratorDFS(object):
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
                nested_list_iterator = FlattenNestedIteratorDFS(elem.getList())
                while nested_list_iterator.has_next():
                    self.queue.append(nested_list_iterator.next())

    def has_next(self):
        return len(self.queue) > 0

    def next(self):
        return self.queue.popleft()


class FlattenNestedIteratorBFS(object):
    """
    BFS用stack，里面存放的是每个元素，以及对应的index，表示如果当前元素是list，里面的nested object index
    开始的时候，是输入的nested list，对应元素0。
    Example: [1, 2, [3, 4, [5], 6], [7, 8], 9]，stack的样子：
    最开始，
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 0
    next之后：
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 1
    next=之后：
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 2
    next之后：找到了新的nested list
    [3, 4, [5], 6], 0
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 3
    next之后：
    [3, 4, [5], 6], 1
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 3
    next之后：
    [3, 4, [5], 6], 2
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 3
    next之后：找到了新的nested list
    注意此时[3, 4, [5], 6]的index从2变成了3，即需要增加一位，因为2位置的已经放到了top，top结束后返回到6，也就是index=3
    [5], 0
    [3, 4, [5], 6], 3
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 3
    next之后：回到了之前的nested list
    [3, 4, [5], 6], 3
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 3
    next之后：回到了之前的nested list
    [1, 2, [3, 4, [5], 6], [7, 8], 9], 3
    """
    def __init__(self, nested_list):
        # LIFO -> top is the latest nested list
        self.stack = [[nested_list, 0]]

    def next(self):
        if self.has_next():
            nested_object, i = self.stack[-1]
            # 更新pop后的top的index+1
            self.stack[-1][1] += 1
            return nested_object[i].getInteger()
        else:
            raise Exception("No more element!")

    def has_next(self):
        while self.stack:
            # i对应的就是当前nested object的之前遍历到的index
            nested_object, i = self.stack[-1]
            if i == len(nested_object):
                # 此时表明，当前nested object的所有元素均被遍历完了（如果是一个int，i=1）
                # 需要pop出stack top，然后继续检查下一个
                self.stack.pop()
            else:
                x = nested_object[i]
                # 如果i还没到头，判断对应元素x是否为int，如果是，说明还有元素
                if x.isInteger():
                    return True
                # 如果对应元素x是nested list，更新top元素y里面的index
                # 即当我们返回到这个y的时候，x作为nested list已经全部被便利完了，要继续遍历y后边的元素，即i+1
                self.stack[-1][1] += 1
                # 以及，之后x作为nested list要从第0个开始遍历
                self.stack.append([x.getList(), 0])
        # 如果中间没有返回，说明所有元素遍历结束，没有next了
        return False


class Flatten2DVector(object):
    """
    https://leetcode.com/problems/flatten-2d-vector/description/
    为一个2D数组设计一个iterator
    Follow up: 如何实现remove方法？
    """
    def __init__(self, vec2d):
        self.row = self.col = 0
        self.vec = vec2d
        self.total_row = len(self.vec)
        self.remove_flag = False

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
        self.remove_flag = True
        return self.vec[self.row][self.col]

    def hasNext(self):
        return self.row < self.total_row and self.col < len(self.vec[self.row])

    def remove(self):
        """
        删除当前iterator遍历到的节点，把它变为None，每次调用前必须调用next方法，以确保有节点可以删除
        """
        if self.remove_flag:
            self.remove_flag = False
            self.vec[self.row][self.col] = None
        else:
            raise ValueError("Need to iterate a new value to be removed")
