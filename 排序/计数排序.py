# -*- coding: utf-8 -*-

from collections import defaultdict


def sort_colors(nums):
    """
    https://leetcode.com/problems/sort-colors/description/
    荷兰国旗问题，0、1、2分别表示红白蓝，按照红白蓝依次排序
    counting sort，按照每一位置排序，每一位的顺序需要预先定义好
    """
    count_array = [0, 0, 0]
    color_array = [0, 1, 2]
    for n in nums:
        count_array[n] += 1
    i = j = 0 # 两个pointers，i指向nums，j指向color count
    while i < len(nums):
        while j < len(count_array) and count_array[j] > 0:
            count_array[j] -= 1
            nums[i] = color_array[j] # 找到对应颜色
            i += 1
        j += 1


def sort_characters_by_frequency(s):
    """
    https://leetcode.com/problems/sort-characters-by-frequency/description/
    按照词频打印，比如bloomberg，最后打印bboomlerg，也就是按照词频来，但是同一个词频的char打印顺序无所谓
    两个hash map，分别记录char->index，以及index->char，遍历每一个char，更新对应的map，类似于计数排序
    空间O(1)，因为这里面只有有限个char，即26个字母，对应的frequency也最多有26种类。时间O(N)
    """
    wc = defaultdict(int)
    wc2 = {}
    res = list([])
    for c in s:
        wc[c] += 1
    for k, v in wc.items():  # reverse
        wc2[v] = wc2.get(v, set([]))
        wc2[v].add(k)
    counts = sorted(wc2.keys(), reverse=True)
    for c in counts:  # from most frequent
        for char in wc2[c]:
            res.append(char * c)
    return "".join(res)
