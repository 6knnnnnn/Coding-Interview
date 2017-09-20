# -*- coding: utf-8 -*-


def can_place_flowers(flower_bed, n):
    """
    https://leetcode.com/problems/can-place-flowers/description/
    给定一个array，里面只有1和0，1代表有花，0代表没有花
    现在要判断是否能种下n朵花在这个array里面，规则是，任意两个花不能相邻
    直接从头扫到位，对于某个位置i，只有出现 i-1 = i = i+1 = 0的时候，才能种花，此时n-1
    其实如果n比flower bed的长度的1/2还要大，就不用判断了
    """
    total, i = len(flower_bed), 0
    while i < total and n > 0:
        if flower_bed[i] == 1:
            i += 1  # i=1
        elif i >= 1 and flower_bed[i - 1] == 1:
            i += 1  # i-1=1, i=0
        elif i < total - 1 and flower_bed[i + 1] == 1:
            i += 1  # i-1=0, i=0, i+1=1
        else:  # i-1=0, i=0, i+1=0, move by 2
            n -= 1
            i += 2
    return n <= 0
