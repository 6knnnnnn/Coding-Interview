# -*- coding: utf-8 -*-

"""
https://leetcode.com/problems/design-phone-directory/description/

也可以用linked list来做，或者用queue，如果顺序很重要的话
"""


class PhoneDirectory(object):
    def __init__(self, maxNumbers):
        self.used = set([])
        self.nums = range(maxNumbers)

    def get(self):
        if len(self.nums) == 0:
            return -1
        num = self.nums.pop()  # FILO
        self.used.add(num)
        return num

    def check(self, number):
        return number not in self.used

    def release(self, number):
        if number in self.used:  # check
            self.used.remove(number)
            self.nums.append(number)

