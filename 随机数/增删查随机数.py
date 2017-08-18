# -*- coding: utf-8 -*-

"""
这道题目在Lintcode中是Load balancer
• 要在o(1)的时间内插入删除,只能hash。那hash可以getRandom吗?
– 不太好做
• 什么数据结构比较好getRandom?
– 数组
• 考虑hash与数组结合起来用,hash插入一个,数组也插入一个。那么问题来了,数组删除元素怎么办?
– 与最后插入的一个元素交换
• 那怎么o(1)时间在数组中找到要删除元素(要交换)的位置?
– 用hash将元素的位置记下来
"""
import random


class RandomizedSet(object):
    # https://leetcode.com/problems/insert-delete-getrandom-o1/description/
    # 这里假设不存在重复元素
    def __init__(self):
        # an array for values, a dict for X
        self.nums, self.pos = [], {}

    def insert(self, val):
        if val in self.pos: # 已经存在了，就返回False
            return False
        # 插入到最后一个，所以index就是n-1
        self.nums.append(val)
        self.pos[val] = len(self.nums) - 1
        return True

    def remove(self, val):
        if val not in self.pos: return False
        # switch with the last one
        val_idx, last_val = self.pos[val], self.nums[-1]
        # 分别更新最后一个元素的在nums中的位置，以及pos中的index
        self.nums[val_idx] = last_val
        self.pos[last_val] = val_idx
        # 删除val对应的nums位置以及pos的key
        self.nums.pop()
        self.pos.pop(val)
        return True

    def get_random(self):
        if self.nums:
            return random.choice(self.nums)


class RandomizedCollection(object):
    # 如果允许重复的怎么办？hash set记录对应val的所有index，map: value -> set([X..])
    def __init__(self):
        self.val_list, self.index_map = list([]), dict([])

    def insert(self, val):
        self.val_list.append(val)
        if val not in self.index_map:
            self.index_map[val] = set([])
        self.index_map[val].add(len(self.val_list) - 1)
        return len(self.index_map[val]) == 1 # 如果有重复就返回False

    def remove(self, val):
        # 把val对应的一个index找到，把最后的last val挪到这个index上去
        # 把last val之前的index=n-1删掉改为val X
        if val in self.index_map:
            remove_index, last_val = self.index_map[val].pop(), self.val_list[-1]
            self.val_list[remove_index] = last_val
            if last_val in self.index_map:
                self.index_map[last_val].add(remove_index)
                self.index_map[last_val].remove(len(self.val_list) - 1)
            self.val_list.pop()
            return True
        return False

    def get_random(self):
        return random.choice(self.val_list)
