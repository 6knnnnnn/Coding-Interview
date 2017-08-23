# -*- coding: utf-8 -*-

# Moving Average from Data Stream
# 用一个queue保存需要的数字
from collections import deque


class MovingAverage(object):
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


def sliding_window_max(nums, k):
    """
    https://leetcode.com/problems/sliding-window-maximum/description/
    窗口内只保留“必要”的元素：双端队列deque存的是index，防止重复value；“过期”机制来pop出不必要的元素
    所有的value，最多进deque一次，最多出deque一次，时间复杂度O(N)
    1. 右边加数划进来
        窗口内必须保证严格递减，如果新进入的value违反严格递减，则pop left出所有比这个value小的值x
        原因：新进来的value比这些pop出的值x都大，而且晚过期（index靠后），不需要在deque中保留这些x
    2. 左边减数划出去
        检查最左边的元素是否“过期”：如果最左的index和当前的窗口最右index距离为K+1，过期，pop出去
    """
    result = []
    if nums and k > 0:
        queue = deque([]) # at most k K
        for i, v in enumerate(nums):
            # check if the 1st expires: X>=i-k+1?
            if queue and queue[0] < i-k+1:
                queue.popleft()
            while queue and nums[queue[-1]] < nums[i]:
                queue.pop() # ensure Monotonic
            queue.append(i) # queue[0,last] Monotonic
            # if i>k-1, window K=k, output the max
            if queue and i >= k - 1:
                result.append(nums[queue[0]])
    return result


def sliding_window_median(nums, k):
    pass