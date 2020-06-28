import random
from collections import defaultdict


class RandomPickWeight(object):
    # https://leetcode.com/problems/random-pick-with-weight/
    def __init__(self, nums):
        self.roll_sum = [nums[0]]
        for i in xrange(1, len(nums)):
            self.roll_sum.append(self.roll_sum[i-1] + nums[i])

    def pickIndex(self):
        target = random.randint(1, self.roll_sum[-1])
        if target < self.roll_sum[0]:
            # edge case check
            return 0
        l, r = 0, len(self.roll_sum) - 1
        while 0 <= l <= r < len(self.roll_sum):
            mid = (l + r) / 2
            mValue = self.roll_sum[mid]
            if mValue == target or (mid-1 >= 0 and self.roll_sum[mid-1] < target < mValue):
                return mid
            if mid+1 < len(self.roll_sum) and mValue < target < self.roll_sum[mid+1]:
                return mid+1
            if mValue > target:
                r = mid - 1
            else:
                l = mid + 1


def test1():
    rpw = RandomPickWeight([3, 5, 3, 9])
    wc = defaultdict(int)
    for i in xrange(1000):
        r = rpw.pickIndex()
        wc[r] += 1
    print wc


class KeyWeight(object):
    def __init__(self, key, weight):
        self.key = key
        self.weight = weight

    def __repr__(self):
        return "{}={}".format(self.key, self.weight)


class RandomPickWeightKey(object):
    def __init__(self, inputs):
        # inputs = [KeyWeight(abc, 12)...]
        self.roll_sum = []
        self.keys = set([])
        for i in xrange(0, len(inputs)):
            accuKW = self.roll_sum[i-1] if i >= 1 else KeyWeight('', 0)
            oldKW = inputs[i]
            newKw = KeyWeight(oldKW.key, oldKW.weight + accuKW.weight)
            self.roll_sum.append(newKw)
            self.keys.add(oldKW.key)

    def pickIndex(self):
        target = random.randint(1, self.roll_sum[-1].weight)
        if target < self.roll_sum[0].weight:
            # edge case check
            return 0
        l, r = 0, len(self.roll_sum) - 1
        while 0 <= l <= r < len(self.roll_sum):
            mid = (l + r) / 2
            mValue = self.roll_sum[mid].weight
            if mValue == target or (mid-1 >= 0 and self.roll_sum[mid-1].weight < target < mValue):
                return mid
            if mid+1 < len(self.roll_sum) and mValue < target < self.roll_sum[mid+1].weight:
                return mid+1
            if mValue > target:
                r = mid - 1
            else:
                l = mid + 1

    def pickIndexKey(self):
        index = self.pickIndex()
        return self.roll_sum[index].key

    def setKey(self, key, weight):
        if key not in self.keys:
            # insert new one
            self.keys.add(key)
            kw = KeyWeight(key, weight + self.roll_sum[-1].weight if self.roll_sum else 0)
            self.roll_sum.append(kw)
        else:
            # find the key and update the roll sum
            i = 0
            while self.roll_sum[i].key != key:
                i += 1
            diff = self.roll_sum[i].weight - weight if i == 0 else\
                self.roll_sum[i].weight - self.roll_sum[i-1].weight - weight
            while i < len(self.roll_sum):
                self.roll_sum[i].weight -= diff
                i += 1


def test2():
    def printWC(rpw):
        wc = defaultdict(int)
        for i in xrange(1000):
            r = rpw.pickIndexKey()
            wc[r] += 1
        print wc

    rpw = RandomPickWeightKey([KeyWeight("k0", 3),
                               KeyWeight("k1", 3),
                               KeyWeight("k2", 5),
                               KeyWeight("k3", 9)])
    printWC(rpw)
    rpw.setKey("k0", 23)
    printWC(rpw)
    rpw.setKey("k4", 40)
    printWC(rpw)


test2()
