# -*- coding: utf-8 -*-
"""
  往一个int array 代表海拔的格子里倒水，打印出倒水后的图， 输入：int[] 海拔， int 水数量， int 倒得位置

  For example:
  heights = [5,4,2,1,2,3,2,1,0,1,2,4]

  +
  ++         +
  ++   +     +
  +++ +++   ++
  ++++++++ +++

  Pour 8 units of water at index 5, then output

       |
       v
  0123456789
  +
  ++         +
  ++www+     +
  +++w+++www++
  ++++++++w+++

  可以和面试官讨论assumptions
  - 水滴优先往左流，没地流再往右流，也没地了就在当前位置涨
  - 两边有无限高的墙挡着（但是可能别的面试官是别的条件）
  - 水滴是一滴一滴的，不能分为小数，所以一滴水会一直往左走到尽头（其实是不符合物理规则的但理他呢。。）

第一步，可能先是根据输入创建一个matrix，用来表达蓄水池
matrix长 = len(heights), 高=max(heights)，但需要考虑左右边界是否有无限高的墙挡着

第二步，对于滴水滴的位置i，要分情况考虑左右两边的高度和i的对比
0. i刚好处于高点，即凸出来了，i位置不可以填水，需要先去看左边的情况，之后再去看右边的情况
1. i刚好处于低估，即凹下去了，i位置可以填水，填到跟左右一样高之后，递归解决
2. i比比右边低，但比左边高，那么要先去左边填水，如果还有剩余，在递归解决
3. i比比右边高，但比左边低，那么要先去右边填水，如果还有剩余，在递归解决

"""


class PourWater(object):
    def __init__(self, heights):
        # 假设两边没有额外的height，即如果到了两边，水可能会流走
        self.walls = [0] + heights[:] + [0]
        self.waters = [0] * len(self.walls)

    def update_bound(self, left_bound, right_bound):
        # 更新墙的两侧height
        self.walls[0] = left_bound
        self.walls[-1] = right_bound

    def pour_at_x(self, x, water_amount):
        walls, water_bar = self.walls, [0] * len(self.walls)
        for i in xrange(len(self.waters)):
            self.waters[i] = 0
        # 因为多了一个left bound，所以x要更新为+1
        x += 1
        while water_amount:
            # 每次只注一滴水，不然情况会变得复杂
            left = x - 1
            while left >= 0:
                # 先去左边，直到左边i比i+1还要高，即先向左找到非递增的最低点
                # 比如 hi=3, wi = 2, i ->     +++++ (横向的表达，可能有水的情况)
                # hi+1 = 2， wi+1 = 1 i+1 ->  ++
                # 此时i不能向左边再继续走了，需要填补i+1
                h1 = walls[left] + water_bar[left]
                h2 = walls[left+1] + water_bar[left+1]
                if h1 > h2:
                    break
                left -= 1
            # left 的右边left+1就是第一个比left矮的，如果这个left+1比x还要矮，说明应该现在这里面注一滴水
            if walls[left + 1] + water_bar[left + 1] < walls[x] + water_bar[x]:
                pour_i = left + 1
            else:
                # 左边结束了，去往右边
                right = x + 1
                while right < len(walls):
                    h1 = walls[right] + water_bar[right]
                    h2 = walls[right-1] + water_bar[right-1]
                    if h1 > h2:
                        break
                    right += 1
                if walls[right - 1] + water_bar[right - 1] < walls[x] + water_bar[x]:
                    pour_i = right - 1
                else:
                    pour_i = x

            water_bar[pour_i] += 1
            water_amount -= 1

    def print_matrix(self):
        # 从底下开始打印wall and water
        bars = [self.walls[i] + self.waters[i] for i in xrange(len(self.walls))]
        max_height = max(bars)
        row = len(self.walls)
        str_list = list([])
        for h in xrange(max_height-1, 0, -1):
            for r in xrange(row):
                if h <= self.walls[r]:
                    str_list.append("+")
                elif h <= self.walls[r] + self.waters[r]:
                    str_list.append("w")
                else:
                    str_list.append(" ")
            str_list.append("\n")
        print "".join(str_list)

H = [5,4,2,1,2,3,2,1,0,1,2,4]
# pw = PourWater(H)
# pw.update_bound(0, 0)
# pw.pour_at_x(5, 14)
# pw.print_matrix()


def pour_water(walls, x, water_amount, left_bound, right_bound):
    water_bars = [0] * len(walls)
    while water_amount:
        # 每次只注一滴水，不然情况会变得复杂
        put_index = left = right = x
        while left >= 1:
            # 先去左边，直到左边i比i+1还要高，即先向左找到非递增的最低点（可能是x本身）
            # 比如 h1=3, i=1 -> +++++ (横向的表达，可能有水的情况)
            # h2 = 2, i+1=2 ->  ++
            h1 = walls[left - 1] + water_bars[left - 1]
            h2 = walls[left] + water_bars[left]
            # 如果找到了h1>h2<=h3<=h4...x，那么h2就是可能的 put index
            if h1 > h2:
                break
            left -= 1
        # h1>h2<=h3<=h4...x，如果这个h2比x还要矮，说明应该现在这里面注一滴水，此时h2=left h1=left-1
        if walls[left] + water_bars[left] < walls[x] + water_bars[x]:
            put_index = left
        else:
            # 左边结束了，去往右边去寻找非递增的最低点
            while right < len(walls)-1:
                h1 = walls[right + 1] + water_bars[right + 1]
                h2 = walls[right] + water_bars[right]
                if h1 > h2:
                    break
                right += 1
            if walls[right] + water_bars[right] < walls[x] + water_bars[x]:
                put_index = right

        water_bars[put_index] += 1
        water_amount -= 1

    # now print
    bars_total = [water_bars[i] + walls[i] for i in xrange(len(walls))]
    highest = max(bars_total)
    str_list = list([])
    for h in xrange(highest-1, -1, -1):
        for r in xrange(len(walls)):
            if h <= walls[r]:
                str_list.append("+")
            elif h <= walls[r] + water_bars[r]:
                str_list.append("w")
            else:
                str_list.append(" ")
        str_list.append("\n")
    print "".join(str_list)


pour_water(H, 5, 9, 0, 0)
