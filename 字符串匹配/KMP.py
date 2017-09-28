# -*- coding: utf-8 -*-


def find_substring(s, t):
    """
    https://leetcode.com/problems/implement-strstr/description/
    在s中找是否有substring等于t，如果有，返回最开始的index，否则返回-1
    最简单的方法，双层for loop
    """
    if not s and not t:
        return 0
    if len(s) >= len(t):
        for i in xrange(len(s)-len(t)+1):
            if s[i: i+len(t)] == t:
                return i
    return -1

