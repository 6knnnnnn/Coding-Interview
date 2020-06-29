# -*- coding: utf-8 -*-


def merge_intervals(intervals):
    """
    https://leetcode.com/problems/merge-intervals/description/
    返回merge后的结果，输入并没有排序。

    Test0: [1, 10], [2, 3] return [1, 10]
    Test1: [1,3],[2,6],[15,18], return [1,6],[8,10],[15,18]
    Test2: [1, 5], [6, 7], return [1, 5], [6, 7]

    follow up:
    1. 如果数据结构不是array而是linked list，仍旧需要排序，其实merge sort的时候就可以进行区间合并
    2. 需要记录merge之后，每个区间，原始的interval个数？加一个field就好了
    """
    merged = list([])
    if intervals:
        # 先排序
        intervals = sorted(intervals, key=lambda x: x.start)
        merged.append(intervals[0])
        for i in xrange(1, len(intervals)):
            curr = intervals[i]
            last = merged[-1]
            if last.end >= curr.start:
                # 结果中最后的结束时间晚于当前的开始时间，此时把当前的merge到last里即可
                # last=(1, 5) curr=(2, 4) -> last=(1, 5)，last肯定比curr早开始，因为已经排好序了
                last.end = max(last.end, curr.end)
            else:
                # 否则，把当前的加到结果里
                merged.append(curr)
    return merged


def insert_interval(intervals, new):
    """
    https://leetcode.com/problems/insert-interval/description/
    input里面没有overlap的情况，而且已经排序，要求插入新的interval，必要时merge

    Test0: [1, 3], [8, 10], new = [4, 5] -> [1, 3], [4, 5], [8, 10]
    Test1: [1, 5], [7, 10], new = [4, 6] -> [1, 6], [7, 10] (merge)
    Test2: [1, 5], [7, 10], new = [4, 7] -> [1, 10] (merge)

    O(N)的做法就是从头扫到尾，找到对应的merge点，merge之后仍要继续，直到不需要在merge了
    或者，根据上一题的方法，先插入，然后直接套用merge interval

    follow up: 如果数据结构不是array而是linked list，遍历的时候其实一个意思，如果是inplace操作反而更省时因为不用extend
    """
    output = list([])
    for i in xrange(len(intervals)):
        x = intervals[i]
        if new.end < x.start:
            # 没有overlap： ... new, x ... ，merge结束了
            output.append(new)
            output.extend(intervals[i:])
            return output
        elif new.start > x.end:
            # 没有overlap ... x.e, new.s... x在new前边结束
            output.append(x)
        elif new.start <= x.end:
            # ... new.start, x.end ... 需要merge
            # x可能在new前边结束，也可能在new前边开始，分别找最大最小的
            new.start = min(x.start, new.start)
            new.end = max(new.end, x.end)
    # 没有直接返回，说明new还没有加入到结果里，new是最后一个
    output.append(new)
    return output
