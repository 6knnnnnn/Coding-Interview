# -*- coding: utf-8 -*-


def book_earliest_room(inputs, days):
    """
    给一个list，list内每个元素是一个起始日期和终止日期。代表起始日期到终止日期内，这个房间是不可用的。
    给一个int数组代表需求使用的房间长度，求能满足这个需求的最早的起始日期
    比如给一个 [[1,3], [5,6]]，想呆1天，则返回3 （1～3，3～4被认为是不重叠的）
    """
    inputs.sort()
    for i in xrange(0, len(inputs)-1):
        room1, room2 = inputs[i], inputs[i+1]
        gaps = room2[0] - room1[1]
        if gaps >= days:
            return room1[1]
    return inputs[-1][1]


inputs = [[1, 3], [10, 15], [5, 6]]
for days in [1, 2, 3, 4, 5, 6]:
    print book_earliest_room(inputs, days)


class Event(object):
    def __init__(self, start, end):
        self.start, self.end = start, end

    def __repr__(self):
        return "{} {}".format(self.start, self.end)


class MyCalendar(object):
    def __init__(self):
        self.events = list([])

    def book(self, start, end):
        assert start < end
        newEvent = Event(start, end)
        for i, existing in enumerate(self.events):
            if end <= existing.start:
                self.events.insert(i, newEvent)
                return True
            elif not start >= existing.end:
                return False
        self.events.append(newEvent)
        return True


from collections import deque


class MyCalendarTwo(object):
    def __init__(self):
        self.events = list([])
        self.maxConflict = 2 # k-1

    def book(self, start, end):
        if start == 25:
            a = 1
        newEvent = Event(start, end)
        conflictQ = deque([])
        for i, existing in enumerate(self.events):
            if end <= existing.start:
                self.events.insert(i, newEvent)
                return True
            elif not start >= existing.end:
                # check the conflict Q, compare each one with existing event
                conflictQ.append(existing)
                if len(conflictQ) == self.maxConflict:
                    while conflictQ and conflictQ[0].end <= existing.start:
                        # pop left until find the 1st conflict with existing, break
                        conflictQ.popleft()
                if len(conflictQ) == self.maxConflict:
                    # cannot continue as reach to the threshold
                    return False
        self.events.append(newEvent)
        return True


inputs = [
    [10, 20],
    [15, 30],
    [20, 40],
    [18, 19],
]

inputs = [[10,20],[50,60],[10,40],[5,15],[5,10],[25,55]]
cal = MyCalendarTwo()
for s, e in inputs:
    print cal.book(s, e)
