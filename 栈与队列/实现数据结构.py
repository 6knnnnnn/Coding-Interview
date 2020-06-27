# -*- coding: utf-8 -*-


class MinStack(object):
    """
    https://leetcode.com/problems/min-stack/description/
    两个list方法：一个记录真实的数据data，另一个记录对应的min是多少
    1. 入栈的时候，如果value比min stack top要大，不变，否则，加入 min stack
    2. 出栈的时候，如果value和min stack top相等，min stack就同样pop，否则min stack不动
    这个方法pop的时候会稍微费一点时间，因为需要额外的比较，但是节省空间，min stack不保存所有的min value

    """
    def __init__(self):
        self.data = list([])
        self.min_so_far = list([])

    def push(self, x):
        self.data.append(x)
        if not self.min_so_far or x <= self.min_so_far[-1]:
            # 此时找到了一个新的min，注意这里面需要判断<=
            self.min_so_far.append(x)

    def pop(self):
        if self.data:
            x = self.data.pop()
            if x == self.min_so_far[-1]:
                # 如果pop出来的数据比min so far相等（不可能小于），pop min list
                self.min_so_far.pop()

    def top(self):
        if self.data:
            return self.data[-1]

    def get_min(self):
        if self.min_so_far:
            return self.min_so_far[-1]


class MinStackOneDS(object):
    def __init__(self):
        self.data = list([])

    def push(self, x):
        # record[0] = actual value, record[1] = min so far
        min_so_far = min(x, self.data[-1][1]) if self.data else x
        self.data.append((x, min_so_far))

    def pop(self):
        if self.data:
            result = self.data.pop()
            return result[0]

    def top(self):
        if self.data:
            return self.data[-1][0]

    def get_min(self):
        if self.data:
            return self.data[-1][1]