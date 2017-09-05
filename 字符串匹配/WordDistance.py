# -*- coding: utf-8 -*-

from collections import defaultdict


def shortest_distance_one_time(words, w1, w2):
    """
    For example, assume that words = ["practice", "makes", "perfect", "coding", "makes"].
    Given word1 = “coding”, word2 = “practice”, return 3.
    Given word1 = "makes", word2 = "coding", return 1.
    https://leetcode.com/problems/shortest-word-distance
    其实考察的是 merge sort的变体：找到对应word的index，merge到一起，每次比较，都是比较相邻的两个不同的word
    比如可能会有 a, a, a, b, b，a, a, b...此时每次都要比较相邻的a和b（不然没有意义）
    """
    word_index = []
    for i in xrange(len(words)):
        if words[i] == w1:
            word_index.append((1, i))
        elif words[i] == w2:
            word_index.append((2, i))
    i, res = 0, len(words) + 1
    while i < len(word_index):
        j = i + 1
        while j < len(word_index) and word_index[j][0] == word_index[i][0]:
            # 双指针，确保i和j指向的是两个不同的word，也就是i和j要跳过连续的相同的word
            i, j = i + 1, j + 1
        if j < len(word_index):
            # 不管word1和word2谁先谁后，总是计算出距离
            res = min(word_index[j][1] - word_index[i][1], res)
            i = j  # 接着从j开始
        else:
            return res
    # 如果res没有更新过，仍旧是len(words)-1，也就是一个极值
    return -1


class WordDistance(object):
    """
    https://leetcode.com/problems/shortest-word-distance-ii
    https://leetcode.com/problems/shortest-word-distance-iii
    需要多次找到word distance，而且可能是两个相同的word。预处理输入，然后每次都类似
    """

    def __init__(self, words):
        # 默认为list，如果key不存在就初始化一个empty list
        self.word_index_map = defaultdict(list)
        for i in xrange(len(words)):
            self.word_index_map[words[i]].append(i)
        self.length=len(words)

    def shortest_distance(self, word1, word2):
        if word1 == word2:
            return self.shortest_distance_same(word1)
        # 这里要处理的边际条件比较多，直接merge因为可以一次性扫完，上边的方法在这里需要两次，需要创建index list
        w1, w2 = self.word_index_map[word1], self.word_index_map[word2]
        res, i, j = self.length, 0, 0
        # w1 and w2 all sorted, and no duplicated
        while i < len(w1) and j < len(w2):
            if w1[i] < w2[j]:
                # w1 smaller than w2
                while i < len(w1) and w1[i] < w2[j]:
                    i += 1
                if i == len(w1):
                    # w1 = [2, 8], w2 = [10]，即此时仍然是需要比较的
                    res = min(res, w2[j]-w1[i-1])
                else:
                    # w1 = [2, 11], w2 = [10]，即此时i>j>i-1，要取三者中最小
                    res = min(res, w1[i]-w2[j])
                    res = min(res, w2[j]-w1[i-1])
            else:
                while j < len(w2) and w1[i] > w2[j]:
                    j += 1
                if j == len(w2):
                    res = min(res, w1[i]-w2[j-1])
                else:
                    res = min(res, w2[j]-w1[i])
                    res = min(res, w1[i]-w2[j-1])
        return res

    def shortest_distance_same(self, word):
        # 直接比较两个相同word的index
        index_list = self.word_index_map[word]
        res = self.length
        for i in xrange(len(index_list)-1):
            res = min(res, index_list[i+1]-index_list[i])
        return res
