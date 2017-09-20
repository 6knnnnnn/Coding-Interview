# -*- coding: utf-8 -*-

"""
出处：http://www.cnblogs.com/grandyang/p/4284205.html
仍使用hash map来记录词频，但这里用二进制的表示来作为key，而非长度为10的string，节省了一定的空间
二进制表示：A=0=00, C=1=01, G=2=10 T=3=11
所以，对于长度为10的序列，总长度为20，对应bit就是20位，就需要一个int即可，作为hash map的key
每次有新的letter从左边出去的时候，bit向左移2位，之后根据新进来的letter，补齐最后2位。
"""


def repeated_dna_sequence_hash(s):
    """
    https://leetcode.com/problems/repeated-dna-sequences/description/
    找到所有出现次数大于1的，且长度为10的DNA序列，最简单的就是hash table计数，时间空间O(N)
    """
    total = 10
    d = {}
    res = []
    for i in xrange(len(s) - total + 1):
        seq = s[i:i + total]
        d[seq] = d.get(seq, 0) + 1
    for k, v in d.items():
        if v > 1:
            res.append(k)
    return res
