# -*- coding: utf-8 -*-


def isomorphic_strings(s, t):
    """
    https://leetcode.com/problems/isomorphic-strings/description/
    两个字符串的字符pattern是否一致，也就是每个字符对应的位置应该一致
    egg = add, foo != bar, paper = title，用hash table检查match
    """
    ds, dt = {}, {}
    if len(s) != len(t):
        return False
    for i, c in enumerate(s):
        if c not in ds:
            ds[c] = t[i]
        elif ds[c] != t[i]:
            return False
        if t[i] not in dt:
            dt[t[i]] = c
        elif dt[t[i]] != c:
            return False
    return True

