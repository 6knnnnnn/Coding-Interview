# -*- coding: utf-8 -*-


class LongestPalindromicSubstring(object):
    def __init__(self):
        self.start = self.maxL = 0

    def brute_force_extend(self, s):
        def extend(s, j, k):
            # extend s
            while j>=0 and k<len(s) and s[j]==s[k]:
                j, k = j - 1, k + 1
            newL = k - j - 1
            if self.maxL < newL: # update longest
                self.start = j + 1
                self.maxL = newL

        if not s or len(s) == 1: return s
        for i in xrange(len(s)-1):
            extend(s, i, i) # if result is odd len
            extend(s, i, i+1) # if result if even len
        return s[self.start : self.start + self.maxL]


def palindromic_substrings():
    """
    https://leetcode.com/problems/palindromic-substrings/description/

    """