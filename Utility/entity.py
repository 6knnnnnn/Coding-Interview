# -*- coding: utf-8 -*-


class TreeNode(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "{} (left={} right={})".format(self.val, self.left, self.right)


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        return "%s->%s" % (self.val, self.next)

    @staticmethod
    def array_to_nodes(array):
        head = ListNode(0)
        temp = head
        for a in array:
            temp.next = ListNode(a)
            temp = temp.next
        return head.next


class Interval(object):
    # 一般都需要将区间按照start从小到大排序，很少会按照end排序
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