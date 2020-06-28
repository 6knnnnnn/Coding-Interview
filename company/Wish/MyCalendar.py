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

