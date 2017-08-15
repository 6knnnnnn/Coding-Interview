# -*- coding: utf-8 -*-

import random
from bisect import bisect_left


class RandomWeight(object):
    # 接口定义
    def __init__(self):
        self.key_list = list([])

    def add_weight(self, key, weight):
        raise NotImplementedError

    def get_next_random(self):
        raise NotImplementedError

    def update_weight(self, key, weight):
        raise NotImplementedError


class RandomWeightBinarySearch(RandomWeight):
    # 节省空间实现的一种方式，空间O(K), K为key的数量
    # 但是get random的时间为时间O(logK)，达不到O(1)
    # 而且更新会很麻烦，最坏情况O(K)，需要把所有key的running weight sum更新
    def __init__(self):
        RandomWeight.__init__(self)
        self.running_weights = list([])
        self.pos_map = dict([]) # 记录的还是index，但是running weight里面的index

    def add_weight(self, key, weight):
        if key in self.pos_map:
            return  # immutable so no change
        self.pos_map[key] = len(self.running_weights)
        self.key_list.append(key)
        weight += self.running_weights[-1]
        self.running_weights.append(weight)

    def get_next_random(self):
        if not self.running_weights:
            return None
        rnd_weight = random.randint(1, self.running_weights[-1])
        # 二叉搜索，找到最近的index，也就是对应的key的值
        # A=10  B=20  C=10  D=30
        #   10,   30,   40,   70
        # 1-10 11-30 31-40 41-70
        # 如果随机值=25, i=1, key=B
        i = bisect_left(a=self.running_weights, x=rnd_weight)
        return self.key_list[i]

    def update_weight(self, key, weight):
        # 如果是升weight或者降weight，在key后边的所有running weight都要更新
        # 如果是删除weight为0，key list中这个key后边的running weight向前挪动，时间复杂度O(K)
        pass


class RandomWeightHash(RandomWeight):
    # 其实跟增删查随机数那道题有点类似，就是更新的时候
    # 如果比原来权重小了，把需要删除的元素放倒后边去然后pop
    # 如果比原来权重大了，直接加到最后
    # 空间换时间，O(K * W)空间，即N= key总数K * 平均权重W，查询O(1)
    # 更新理论上最坏情况O(W)，也就是对应key的weight为多少
    def __init__(self):
        RandomWeight.__init__(self)
        self.pos_map = dict([])

    def add_weight(self, key, weight):
        if key in self.pos_map:
            self.update_weight(key, weight)
        else:
            self.pos_map[key] = set([])
            for _ in xrange(weight):
                self.pos_map[key].add(len(self.key_list))
                self.key_list.append(key)

    def get_next_random(self):
        rnd_index = random.randint(0, len(self.key_list) - 1)
        return self.key_list[rnd_index]

    def swap_last_and_pop(self, key):
        if not self.key_list:
            return
        last_val = self.key_list[-1]
        key_index = self.pos_map[key].pop()
        self.key_list[key_index] = last_val
        self.key_list.pop()

    def update_weight(self, key, weight):
        # 权重就是key所在val list中的个数，也就是index的个数
        old_weight = len(self.pos_map[key])
        if weight == 0:
            # 删除key
            while key in self.pos_map:
                self.swap_last_and_pop(key)
        elif weight > old_weight:
            # increase weight 直接加到最后
            while weight > old_weight:
                self.pos_map[key].add(len(self.key_list))
                self.key_list.append(key)
                weight -= 1
        elif weight < old_weight:
            # 减去weight
            while weight < old_weight:
                old_weight -= 1
                self.swap_last_and_pop(key)
