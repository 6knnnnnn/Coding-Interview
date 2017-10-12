# -*- coding: utf-8 -*-

"""
两个字符串一样长的时候，说明有一个替换操作，我们只要看对应位置是不是只有一个字符不一样就行了
一个字符串比另一个长1，说明有个增加或删除操作，我们就找到第一个对应位置不一样的那个字符
如果较长字符串在那个字符之后的部分和较短字符串那个字符及之后的部分是一样的，则符合要求
如果两个字符串长度差距大于1，肯定不对
"""

from collections import defaultdict


def is_one_edit_distance(s, t):
    # https://leetcode.com/problems/one-edit-distance/description/
    # 分情况：如果长度相等，看是否能够modified？如果长度差一，看是否能够delete？否则肯定是False
    def is_one_modified(s, t):
        modified = False
        for i in xrange(len(t)):
            if s[i] != t[i]:
                if modified: # 第二次modified了
                    return False
                modified = True
        return modified

    def is_one_delete(longer, short):
        for i in xrange(len(short)):
            if longer[i] != short[i]:
                # the 1st different, compare the rest
                return longer[i + 1:] == short[i:]
        return True

    if abs(len(s) - len(t)) > 1: return False
    if len(s) == len(t):  # same length
        return is_one_modified(s, t)
    return is_one_delete(s, t) if len(t) < len(s) \
        else is_one_delete(t, s)


def shortest_distance_one_time_no_space(words, w1, w2):
    """
    O(1) space and O(N) time complexity，此时的关键点就是，如何处理edge case：
    1）重复的连续一段序列，找到最后一个
    2）再找到w1的last index i之后，需要找w2 first index j，此时i和j中间的位置k，不能再次出现w1，如果有的话，需要从k再次开始loop
    """
    # use two pointers
    i, res = 0, len(words) + 1
    while i < len(words):
        while i < len(words) and words[i] != w1 and words[i] != w2:
            i += 1
        if i < len(words):
            if words[i] == w2:
                w1, w2 = w2, w1
            # swap w1 and w2 so we now find w1 and need to find w2
            while i < len(words) - 1 and words[i + 1] == w1:
                # move i to the last w1 in current segment of duplicated w1
                i += 1
            # now i is the last w1, i+1 != w1, let's find the next w2
            # if we meet another w1 during this process, i.e. since i+2 to current k
            # we have another w1 but no w2 yet, have to stop and start over to the next loop
            j = i + 1
            while j < len(words) and words[j] != w2 and words[j] != w1:
                j += 1
            if j < len(words) and words[j] == w2:
                # now we find the first w2 after the last w1, and no w1 in between
                res = min(res, j - i)
            i = j  # update i by j position
    return res


def shortest_distance_one_time(words, w1, w2):
    """
    For example, assume that words = ["practice", "makes", "perfect", "coding", "makes"].
    Given word1 = “coding”, word2 = “practice”, return 3.
    Given word1 = "makes", word2 = "coding", return 1.
    https://leetcode.com/problems/shortest-word-distance
    其实考察的是 merge sort的变体：找到对应word的index，merge到一起，每次比较，都是比较相邻的两个不同的word
    比如可能会有 a, a, a, b, b，a, a, b...此时每次都要比较相邻的a和b（不然没有意义）
    所以会有 a -> 0, 1, 2, 5, 6
            b -> 3, 4, 7
    """
    index1, index2 = [], []
    for i in xrange(len(words)):
        if words[i] == w1:
            index1.append(i)
        elif words[i] == w2:
            index2.append(i)
    res = len(words) + 1
    i = j = 0
    while i < len(index1) and j < len(index2):
        res = min(res, abs(index1[i] - index2[j]))
        # 每次移动两者中较小的index
        if index1[i] < index2[j]:
            i += 1
        else:
            j += 1
    # 如果res没有更新过，仍旧是len(words)+1，也就是一个极值
    return -1 if res == len(words) + 1 else res


class WordDistance(object):
    """
    https://leetcode.com/problems/shortest-word-distance-ii
    https://leetcode.com/problems/shortest-word-distance-iii
    需要多次找到word distance，而且可能是两个相同的word。预处理输入，然后每次都类似
    O(N)空间，O(M)时间，M为两个单词出现在words里面的次数。
    """

    def __init__(self, words):
        # 默认为list，如果key不存在就初始化一个empty list
        self.word_index_map = defaultdict(list)
        for i, w in enumerate(words):
            self.word_index_map[w].append(i)
        self.length = len(words)

    def shortest_distance(self, word1, word2):
        if word1 == word2:
            return self.shortest_distance_same(word1)
        # 这里要处理的边际条件比较多，直接merge因为可以一次性扫完，上边的方法在这里需要两次，需要创建index list
        index1, index2 = self.word_index_map[word1], self.word_index_map[word2]
        res, i, j = self.length, 0, 0
        # index1 and index2 all sorted, and no duplicated
        while i < len(index1) and j < len(index2):
            res = min(res, abs(index1[i] - index2[j]))
            # 每次移动两者中较小的index
            if index1[i] < index2[j]:
                i += 1
            else:
                j += 1
        return -1 if res == self.length else res

    def shortest_distance_same(self, word):
        # 直接比较两个相同word的index
        index_list = self.word_index_map[word]
        res = self.length
        for i in xrange(len(index_list)-1):
            res = min(res, index_list[i+1]-index_list[i])
        return res
