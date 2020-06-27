# -*- coding: utf-8 -*-


class RLEIterator(object):
    # https://leetcode.com/problems/rle-iterator/
    # 关键就是记录count和value分开，以及何时更新index、n以及count
    def __init__(self, inputs):
        # process inputs
        self.inputs = inputs
        self.countIndex = 0
        self.count = []
        self.value = []
        self.currentIndex = 0
        i = 0
        while i < len(inputs):
            self.count.append(inputs[i])
            self.value.append(inputs[i+1])
            i += 2

    def next(self, n):
        while self.currentIndex < len(self.count) and n > 0:
            countCopy = self.count[self.currentIndex]
            # update count and n by deducting n, but must be >= 0
            self.count[self.currentIndex] = max(0, countCopy - n)
            n -= countCopy
            if n > 0:
                # n not exhausted yet
                self.currentIndex += 1

        return -1 if n > 0 else self.value[self.currentIndex]

    def nextSimple(self, n):
        while self.countIndex < len(self.inputs) and n > 0:
            countCopy = self.inputs[self.countIndex]
            self.inputs[self.countIndex] = max(0, countCopy - n)
            n -= countCopy
            if n > 0:
                self.countIndex += 2

        return -1 if n > 0 else self.inputs[self.countIndex+1]



iterator = RLEIterator([3,8,0,9,2,5])
for i in [2, 1, 1, 2]:
    print iterator.next(i), iterator.nextSimple(i)