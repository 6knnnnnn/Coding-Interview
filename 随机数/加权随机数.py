# -*- coding: utf-8 -*-

import random
from bisect import bisect_left


class RandomWeight(object):
    # 接口定义
    def __init__(self):
        pass

    def add_weight(self, key, weight):
        raise NotImplementedError

    def get_next_random(self):
        raise NotImplementedError


class ImmutableBinarySearch(RandomWeight):

    def __init__(self):
        RandomWeight.__init__(self)
        self.key_set = set([])
        self.key_list = list([])
        self.running_weights = list([])

    def add_weight(self, key, weight):
        if key in self.key_set:
            return  # immutable so no change
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
        # 如果随机值=25, i=1, key=B, 时间O(logN), 空间O(M), M为key的数量
        i = bisect_left(a=self.running_weights, x=rnd_weight)
        return self.key_list[i]


class MutableHash(RandomWeight):
    # 其实跟增删查随机数那道题有点类似，就是更新的时候
    # 如果比原来权重小了，把需要删除的元素放倒后边去然后pop
    # 如果比原来权重大了，直接加到最后
    def __init__(self):
        RandomWeight.__init__()
        self.pos_map = dict([])
        self.val_list = list([])

    def add_weight(self, key, weight):
        if key in self.pos_map:
            self.update_weight(key, weight)
        else:
            self.pos_map[key] = set([])
            for _ in xrange(weight):
                self.pos_map[key].add(len(self.val_list))
                self.val_list.append(key)

    def get_next_random(self):
        rnd_index = random.randint(0, len(self.val_list)-1)
        return self.val_list[rnd_index]

    def update_weight(self, key, weight):
        raise NotImplementedError


