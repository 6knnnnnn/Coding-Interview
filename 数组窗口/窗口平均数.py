# -*- coding: utf-8 -*-

# Moving Average from Data Stream
# 用一个queue保存需要的数字


from collections import deque


class MovingAverage(object):
    """
    https://leetcode.com/problems/moving-average-from-data-stream
    用一个queue保存需要的数字
    """
    def __init__(self, size):
        self.size = size
        self.queue = deque([])
        self.sum = 0.0

    def next(self, val):
        self.queue.append(val)
        self.sum += val
        if len(self.queue) > self.size:
            self.sum -= self.queue.popleft()
        return self.sum / self.size
