# -*- coding: utf-8 -*-


"""
 设计一个银行帐户系统，实现：
 存钱（帐户id，存钱数目，日期）
 取钱（帐户id，存钱数目，日期）
 查账（帐户id，起始日期，结束日期）： 只需要返回两个数值，一个是起始日期的balance，一个是结束日期的balance。
 描述就是这么多，剩下的自己发挥。钱的类型用integer，日期什么的自定义，我直接拿了integer
"""


class Account(object):
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
        self.history = list([])

    def add(self, value, timestamp):
        self.balance += value
        self.history.append((timestamp, self.balance))
        return True

    def deduct(self, value, timestamp):
        if value <= self.balance:
            self.balance -= value
            self.history.append((timestamp, self.balance))
            return True
        else:
            raise Exception("Invalid amount to withdraw")

    def get_balance_statement(self, start_time, end_time):
        # 用二分查找找到开始点和截止点 index，假设start_time < end_time，而且每次插入都是按照时间大小来的
        def binary_search(target_time):
            l, r = 0, len(self.history)
            while l < r:
                mid = (l+r) >> 1
                if self.history[mid][0] == target_time:
                    return mid
                elif self.history[mid][0] > target_time:
                    r = mid - 1
                else:
                    l = mid + 1
            return l
        start_index = binary_search(start_time)
        end_index = binary_search(end_time)
        if start_index != end_index:
            return [self.history[start_index], self.history[end_index]]
        return [self.history[start_index]]


class BankSystem(object):
    def __init__(self):
        self.account_map = dict([])

    def deposit(self, account_id, amount, timestamp):
        if account_id not in self.account_map:
            self.account_map[account_id] = Account(account_id)
        return self.account_map[account_id].add(amount, timestamp)

    def withdraw(self, account_id, amount, timestamp):
        if account_id not in self.account_map:
            return False
        return self.account_map[account_id].deduct(amount, timestamp)

    def check(self, account_id, start_time, end_time):
        if account_id not in self.account_map:
            return False
        return self.account_map[account_id].get_balance_statement(start_time, end_time)
