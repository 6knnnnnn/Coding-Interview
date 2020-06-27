# -*- coding: utf-8 -*-


class Event(object):
    def __init__(self, s, e):
        self.start = s
        self.end = e

    def __repr__(self):
        return "[{}, {}]".format(self.start, self.end)


class MyCalendar(object):
    # https://leetcode.com/problems/my-calendar-i/
    # 只需要判断是否能够book，本质上就是insert sort
    def __init__(self):
        self.events = list([])

    def __repr__(self):
        return ",".join(self.events)

    def book(self, start, end):
        newEvent = Event(start, end)
        for i, existing in enumerate(self.events):
            if start < existing.start:
                if end <= existing.start:
                    # find the right place to insert this new event
                    self.events.insert(i, newEvent)
                    return True
                # otherwise, conflict
                return False
            if existing.start <= start < existing.end:
                return False
        # finished all the check, append the new one to the end
        self.events.append(newEvent)
        return True

    def bookWithConflict(self, start, end, conflictThreshold=2):
        newEvent = Event(start, end)
        i, conflictPool = 0, list([])
        while i < len(self.events) and end > self.events[i].start:
            if start < self.events[i].end:
                # new event conflict with current event, two cases:
                # 1) e.start <= start < e.end <= end 2) e.start <= start < end < e.end
                conflictPool.append(self.events[i])
            i += 1
        # finished all the check, insert the new one to the right position if not reach threshold
        if len(conflictPool) < conflictThreshold:
            self.events.insert(i, newEvent)
            return True
        # calculate the actual max conflict in conflict pool, if more than threshold, return False
        actualConflictCount = 0

        return len(conflictPool) < conflictThreshold


def test1():
    cal1 = MyCalendar()
    inputs = [(10, 20), (15, 25), (20, 30), (40, 50), (5, 10), (25, 35), (25, 45)]
    for s, e in inputs:
        print s, e, cal1.book(s, e)

def test2():
    cal = MyCalendar()
    inputs = [(10, 20), (50, 60), (10, 40), (5, 15), (5, 10), (25, 55)]
    for s, e in inputs:
        print s, e, cal.bookWithConflict(s, e, 2)


def test3():
    cal = MyCalendar()
    inputs = [[47, 50], [1, 10], [27, 36], [40, 47], [20, 27], [15, 23], [10, 18], [27, 36], [17, 25],
     [8, 17], [24, 33], [23, 28], [21, 27], [47, 50], [14, 21], [26, 32], [16, 21], [2, 7],
     [24, 33], [6, 13], [44, 50], [33, 39], [30, 36], [6, 15], [21, 27], [49, 50], [38, 45],
     [4, 12], [46, 50], [13, 21]]
    expected = [True,True,True,True,True,True,True,True,False,False,False,False,False,True,False,False,False,True,False,False,False,False,False,False,False,False,True,False,False,False]
    i = 0
    for s, e in inputs:
        if i == 9:
            print i
        result = cal.bookWithConflict(s, e)
        if expected[i] != result:
            print i, s, e, expected[i]
        i += 1

test3()
