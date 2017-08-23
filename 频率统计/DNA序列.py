# -*- coding: utf-8 -*-


def repeated_dna_sequence_hash(s):
    """
    https://leetcode.com/problems/repeated-dna-sequences/description/
    找到所有出现次数大于1的长度为10的DNA序列，最简单的就是hash table计数，时间空间O(N)
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
