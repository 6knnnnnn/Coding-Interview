# -*- coding: utf-8 -*-

"""
DFS + pruning 剪枝
搜索到某种情况后，后边的情况肯定都不成立，不再继续搜索
"""


def valid_word_square(words):
    """
    https://leetcode.com/problems/valid-word-square
    :param words:
    :return:
    """
    def check(words, i):
        j = 0
        for c in words[i]:
            if j == len(words) or i >= len(words[j]) or c != words[j][i]:
                return False
            j += 1

        return True

    for i in xrange(len(words)):
        if not check(words, i):
            return False
    return True


def word_square(words):
    """

    :param words:
    :return:
    """
