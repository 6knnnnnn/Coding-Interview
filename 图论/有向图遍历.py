# -*- coding: utf-8 -*-


def course_schedule(n, prerequisites):
    """
    https://leetcode.com/problems/course-schedule/description/
    总共n门课程，有一些课程需要先修课，比如[c1, c2]表示，c2是c1的先修课
    给定所有可能的先修课程关系array，判断是否能够完成n门课程
    其实就是遍历Graph的节点，然后判断是否有环，但此时是有向图，因为先修关系是有方向的edge[0] <- edge[1]
    """


def course_schedule_order(n, prerequisites):
    """
    https://leetcode.com/problems/course-schedule-ii/description/
    类似上边的题，这里要返回的是，可能的一种选课的顺序 the ordering of courses you should take to finish all courses.
    There may be multiple correct orders, you just need to return one of them.
    If it is impossible to finish all courses, return an empty array.
    """


def alien_dictionary(words):
    """
    https://leetcode.com/problems/alien-dictionary/description/
    给定一组单词，已经按照外星人的规则排序好的，求出这个外星人词典的字母顺序
    比如["wrt","wrf","er","ett","rftt"] => 那么字母顺序就是 "wertf"
    可能会有多个结果，即有几个字母的顺序无法决定（同一层），那么返回其中一个可能结果即可。如果有环，则返回""
    1. 根据输入的word，创建graph；2. DFS or BFS，找到topological顺序
    这道题目只存在一个联通分量，也就是整个图，因为给的input是word list，每个char都是存在于graph里面的
    而且这道题目是single source，也就是第一个word的第一个letter
    本道题目的关键点就是：1. 如何建graph 2. node有三种状态 2. 最后生成的order是逆序的，DFS走到了尽头，即顺序最小的node
    如果是BFS，需要从第一个word的第一个char开始，最后得到的顺序就是正序的
    """
    def dfs_has_cycle(graph, node, visited, visiting, order):
        # 检验访问到当前node的时候，是否成环
        # 每个node有三种状态，还没有visit，从某个节点出发到当前node正处于visiting中还没结束，或者之前已经visited了
        if node in visiting:
            # 如果当前node已经处于visiting状态了，又回到了自己，说明有环
            return True
        visiting.add(node)

        for adj in graph[node]:
            if adj not in visited and dfs_has_cycle(graph, adj, visited, visiting, order):
                # 对于那些在之前还没有被visited过的 adj node，检查是否有环
                return True
        # 当前node visiting结束，加入到visited，同时
        visiting.remove(node)
        visited.add(node)
        order.append(node)

    # build adj list graph，这里面key = 字母，value 就是 adj list，这里的adj是direct adj
    graph = {node: [] for node in set(''.join(words))}
    # 这里zip的作用就是，从第一个开始，把word i 和 i + 1组成一个pair
    # 比如 [('wrt', 'wrf'), ('wrf', 'er'), ('er', 'ett'), ('ett', 'rftt')]
    word_pair = zip(words[:-1], words[1:])
    for v, w in word_pair:
        for i in xrange(min(len(v), len(w))):
            if v[i] != w[i]:
                # 这里就是把对应index的w加入到v的adj中去，代表v[i] -> w[i]，即v[i]在前
                graph[v[i]].append(w[i])
                break
    # 用topological sort返回最后的order
    order, visited, visiting = [], set([]), set([])
    for node in graph:
        if node not in visited and dfs_has_cycle(graph, node, visited, visiting, order):
            # 如果有环出现，立刻返回""
            return ''
    # 此时order记录的是逆序，所以返回的是再次逆序order之后的正序结果
    return ''.join(order[::-1])


words = ["wrt", "wrf", "er", "ett", "rftt"]

# print alien_dictionary(words)
