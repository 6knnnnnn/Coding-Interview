# -*- coding: utf-8 -*-
"""
 https://en.wikipedia.org/wiki/Collatz_conjecture
 考拉兹猜想
 给你公式，比如偶数的话除2，奇数的话就变成3*n+1，对于任何一个正数，数学猜想是最终他会变成1。
 每变一步，步数加1，给一个上限n，让找出范围内最长步数

 记忆化搜索

 这题如果follow up还可以考虑输出最长的序列，那么我们就需要一个map来保存 integer -> list(integer)

 比如：
    n = 3  -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
    n = 6，得出序列6, 3, 10, 5, 16, 8, 4, 2, 1。(步骤中最高的数是16，共有8个步骤)
    n = 11，得出序列11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1。(步骤中最高的数是52，共有14个步骤)
"""


def find_sequence_length(n):
    def search_steps(cache_steps, x):
        if x not in cache_steps:
            new_x = x / 2 if x != 0 and x % 2 == 0 else 3 * x + 1
            # 找到历史记录，然后+1，就是对应的x的步骤数目
            steps = search_steps(cache_steps, new_x)
            cache_steps[x] = steps + 1
        return cache_steps[x]

    # 初始化1->0
    cache_steps = {1: 0}
    for i in xrange(n+1):
        search_steps(cache_steps, i)
    return max(cache_steps.values())


def find_sequence(n):
    def search_sequence(cache_seq, x):
        if x not in cache_seq:
            new_x = x / 2 if x != 0 and x % 2 == 0 else 3 * x + 1
            seq = search_sequence(cache_seq, new_x)
            cache_seq[x] = [new_x] + seq
        return cache_seq[x]

    # 初始化1->[]
    cache_seq = {1: []}
    for i in xrange(n+1):
        search_sequence(cache_seq, i)
    longest = []
    target = 1
    for i, l in cache_seq.items():
        if len(l) > len(longest):
            longest = l
            target = i
    return target, longest

print find_sequence(6)
print find_sequence(11)
