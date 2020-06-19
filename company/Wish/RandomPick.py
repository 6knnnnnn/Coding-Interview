import random
from collections import defaultdict


class ValueIndexPair(object):
    def __init__(self, index, value):
        self.value = value
        self.index = index

    def __str__(self):
        return "v={}; i={}".format(self.value, self.index)


class Solution(object):
    def __init__(self, nums):
        self.data = [ValueIndexPair(i, n) for i, n in enumerate(nums)]
        self.data.sort(key= lambda x: x.value)
        self.gaps = []
        for i in xrange(1, len(self.data)):
            gap = self.data[i].value - self.data[i - 1].value
            self.gaps.append(gap)
            if len(self.gaps) >= 2:
                self.gaps[-1] += self.gaps[-2]

    def pickIndex(self):
        index = random.randint(0, self.gaps[-1]+1)
        if index <= self.gaps[0]:
            return self.gaps[0]
        l, r = 0, len(self.gaps)
        while 0 <= l <= r < len(self.gaps):
            mid = (l + r) / 2
            if self.gaps[mid] == index:
                return self.gaps[mid]
            if mid - 1 >= 0 and self.gaps[mid-1] < index < self.gaps[mid]:
                return self.gaps[mid]
            if mid + 1 < len(self.gaps) and self.gaps[mid] < index < self.gaps[mid + 1]:
                return self.gaps[mid + 1]
            if index > self.gaps[mid]:
                l = mid + 1
            else:
                r = mid - 1
        return None

a = [1, 17, 5, 20]
sol = Solution(a)
print sol.gaps
wc = defaultdict(int)
for i in xrange(100):
    index = sol.pickIndex()
    wc[index] += 1
print wc
