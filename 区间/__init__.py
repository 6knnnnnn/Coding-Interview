# -*- coding: utf-8 -*-

# 一般都需要将区间按照start从小到大排序，很少会按照end排序


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return "({}, {})".format(self.start, self.end)

    @staticmethod
    def list_to_interval(input_list):
        interval_list = list([])
        for input in input_list:
            interval_list.append(Interval(input[0], input[1]))
        return interval_list

    @staticmethod
    def get_start_key(interval):
        return interval.start

    @staticmethod
    def get_end_key(interval):
        return interval.end