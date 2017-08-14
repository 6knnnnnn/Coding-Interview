# -*- coding: utf-8 -*-


# Given a string, find the first non-repeating character in it and return it's index. If it doesn't exist, return -1.
def first_unique_char(s):
    # https://leetcode.com/problems/first-unique-character-in-a-string/description/
    d = {}
    for i in xrange(len(s)):
        d[s[i]] = len(s) if s[i] in d else i
    first = len(s)
    for k in d:
        first = min(first, d[k])
    return first if first < len(s) else -1



