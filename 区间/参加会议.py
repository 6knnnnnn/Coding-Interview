# -*- coding: utf-8 -*-

from 区间 import Interval

# Given a collection of intervals, find the min number of intervals need to remove
# to make the rest of the intervals non-overlapping.
# 其实就是经典的activity selection问题，按照end时间排序后，贪心算法
# Find the activity compatible with the previous selected activity and with the earliest finishing time,
# so the there will be maximum resources for the remained activities after this one
# 即这里并非erase，而是select，最后的结果就是尽可能多的兼容的interval，换言之就是erase最少的interval


def erase_overlap_intervals(intervals):
    # 最初为负无穷，可能有负数
    intervals = sorted(intervals, key=lambda i: i.end)
    prev = intervals[0]
    erased = 0
    for i in xrange(1, len(intervals)):
        if intervals[i].start >= prev.end:
            # 此时说明，i开始前prev已经结束了，没有overlap，不需要删除掉当前节点
            # 比如prev = [8, 10], i = [15, 20]
            # 如果是activity selection，此时要把i加入到结果中
            prev = intervals[i]
        else:
            # 此时，i开始前prev还没结束，有overlap，需要删除掉i
            # 比如 prev = [8, 10], i = [5, 20]
            erased += 1
    return erased


def has_meeting_overlap(interval_list):
    # https://leetcode.com/problems/meeting-rooms/description/
    # 判断一个人是否能参加所有的meeting：按照start排序后，看相邻两个interval之间有没有overlap
    sorted(interval_list, key=Interval.get_start_key)
    for i in xrange(1, len(interval_list)):
        prev, curr = interval_list[i-1], interval_list[i]
        if prev.start > curr.end:
            return True
    return False


def min_meeting_rooms(interval_list):
    # https://leetcode.com/problems/meeting-rooms-ii/description/
    start, end = list([]), list([])
    for i in interval_list:
        start.append(i.start)
        end.append(i.end)
    start.sort()
    end.sort()
    available = total = i = j = 0
    # 需要排序是因为要有一个同一的时间来对比不同会议之间结束和开始的关系
    # i和j分别是start和end的指针，遍历所有的start时间
    # 1）如果j结束前i开始了，有冲突，start[i] < end[j]，需要安排一个会议室
    #    如果没有available的room，需要寻找一个新的，总数+1，否则available-1，挪动i
    #    即便刚好start和end的i位置指向的是同一个meeting，那么肯定也是一个新的meeting，需要安排一个room
    # 2）否则j结束后i才开始，无冲突，start[i] >= end[j]，一个meeting结束了，available+1
    while i < len(start):
        if start[i] < end[j]:
            if available > 0:
                available -= 1
            else:
                total += 1
            i += 1
        else:
            available += 1
            j += 1
    return total


sample = [[1,2], [2,5], [4,5]]

interval_list = Interval.list_to_interval(sample)

print min_meeting_rooms(interval_list)