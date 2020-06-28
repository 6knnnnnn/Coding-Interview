from heapq import *


class MedianDataStream(object):
    def __init__(self):
        self.left = [] # max heap, invert min heap
        self.right = [] # min heap

    def findMedian(self):
        if len(self.left) == len(self.right):
            # left is max heap, invert value
            return (self.right[0] - self.left[0]) / 2.0
        return self.right[0]

    def addNum(self, num):
        # add a new number depends on the size of left and right heap
        if len(self.left) == len(self.right):
            # insert to the left one, then re-balance, and insert to the right one
            val = heappushpop(self.left, -num)
            heappush(self.right, -val)
        else:
            # right size - left size = 1, insert to right one, pop and insert to left
            val = heappushpop(self.right, num)
            heappush(self.left, -val)

    def __repr__(self):
        return "left={}         right={}".format(self.left, self.right)


def test1(inputs):
    mds = MedianDataStream()
    for i in inputs:
        mds.addNum(i)
        print mds.findMedian()


test1(range(1, 11))
test1([-1, -2, -3, -4, -5])
