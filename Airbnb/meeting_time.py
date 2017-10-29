# -*- coding: utf-8 -*-
"""
  给一组meetings(每个meeting由start和end时间组成)。求出在所有输入meeting时间段内没有会议，也就是空闲的时间段.
  每个subarray都已经sort好。N个员工，每个员工有若干个interval表示在这段时间是忙碌的。求所有员工都不忙的intervals。
  For example:
  [
   [[1, 3], [6, 7]],
   [[2, 4]],
   [[2, 3], [9, 12]]
  ]
  Output
  [[4, 6], [7, 9]]

  这道题目有点类似于meeting room ii，也就是找到需要多少件meeting room
  但是这里面我们已经知道了meeting room的总数，需要找的是哪个时间段所有的room都没有会议
  （每个员工也就相当于是一个meeting room，同一个room不可能有两个meeting同时进行）

  这题最简单的方法就是把所有区间都拆成两个点，然后排序，然后扫描
  每次碰到一个点如果是左端点就把busy_employees加1，否则减1
  等到每次busy_employees为0时就是一个新的区间
  这样复杂度O(MlogM)，M是总共区间数。

  follow up: 求不少于k个员工空闲的时间段（改一下check count的条件就可以了）
"""


def find_no_meeting_time(meeting_times, k=None):
    start, end, free_time = [], [], []
    free_employees = len(meeting_times)
    # k就是不少于多少员工的follow up，默认为总员工数目
    if k is None:
        k = len(meeting_times)
    for employee_mt in meeting_times:
        for mt in employee_mt:
            start.append(mt[0])
            end.append(mt[1])
    start.sort()
    end.sort()
    i = j = 0
    while i < len(start):
        if start[i] < end[j]:
            # 此时说明，一个employee还没结束meeting j，另一个employee开始了meeting i
            free_employees -= 1
            i += 1
        else:
            # start[i] >= end[j]
            # 此时说明，一个employee结束了meeting j，另一个employee还没开始meeting i
            free_employees += 1
            if free_employees >= k and end[j] != start[i]:
                # 此时说明，有k个员工现在没有在开会，需要记录下来此时的end[j] ... start[i]
                # 即这个时间段，就是满足至少有k个员工没有开会的时间（也就是必须满足start[i] >= end[j]）
                free_time.append([end[j], start[i]])
            j += 1
    return free_time

sample = [
    [[1, 3], [6, 7]],
    [[2, 4]],
    [[2, 3], [9, 12]]
]

res = find_no_meeting_time(sample)
print res

"""
10am - 4pm

5 coding interviews 1 vs 1, 45 mins, lunch break in between by an engineer

shadow interviewer

avoid pseudocode

timeline
"""
