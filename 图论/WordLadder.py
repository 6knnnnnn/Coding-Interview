# -*- coding: utf-8 -*-

from collections import deque


def word_ladder(begin_word, end_word, word_list):
    """
    https://leetcode.com/problems/word-ladder/description/
    Given: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
    As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog", return its length 5.
    假设：如果不存在这么一个编辑方式，返回0；所有的word长度一样
    本质上就是无方向+有环图遍历undirected cyclic graph，从一个source遍历到destination，找到shortest single source path
    把word list改为set，用来判断是否visited，避免cycle。空间为O(N)，时间为O(26 * L * N)，L为每个word的长度
    """
    word_set = set(word_list)
    queue = deque((begin_word, 1))
    fixed_length = len(begin_word)
    while queue:
        curr_word, distance = queue.popleft()
        if curr_word == end_word:
            return distance
        new_distance = distance + 1
        for i in xrange(fixed_length):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                # permutation a new word
                next_word = "%s%s%s" % (curr_word[i:], c, curr_word[i+1:])
                if next_word in word_set:
                    # 挪出visited word，避免环
                    word_set.remove(next_word)
                    queue.append((next_word, new_distance))
    return 0


class WordNode(object):
    # 一个全局变量用来记录所有word的从begin开始的最短距离
    distance_map = dict()

    def __init__(self, word):
        # word本身，距离source distance，是否visited过，所有的相邻node
        self.word = word
        self.visited = False
        if word not in WordNode.distance_map:
            # 1000只是一个placeholder，即假设距离最多有1000个node
            WordNode.distance_map[word] = 1000

    def __repr__(self):
        return "%s %s" % (self.word, WordNode.distance_map[self.word])

    def generate_neighbors(self, i, word_set):
        # 给定某个index，返回在这个index位置上边，可能的所有new word组合，且这个new word必须存在于word set中
        neighbors_word_list = list([])
        if 0 <= i < len(self.word):
            distance = WordNode.distance_map[self.word]
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = "%s%s%s" % (self.word[i:], c, self.word[i+1:])
                if new_word in word_set:
                    # 合法的word，检查他的distance是否需要更新，即更新最短的距离
                    new_distance = min(distance + 1, WordNode.distance_map[new_word])
                    WordNode.distance_map[new_word] = new_distance
                    neighbors_word_list.append(WordNode(new_word))
        return neighbors_word_list


def word_ladder_all_paths(begin_word, end_word, word_list):
    """
    https://leetcode.com/problems/word-ladder-ii/description/
    找到从begin->end所有可能的shortest path，其他规则都一样
    0. 调用word ladder API，找到最小的路径长度min_length
    1. 建立Word Graph，并根据source来更新distance
    2. 从source node开始，对于每个word node而言：
        1）遍历所有的相邻节点，降临时的path保存，当遇到end word的时候，判断是否比更小的

    """