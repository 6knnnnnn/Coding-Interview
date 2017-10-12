# -*- coding: utf-8 -*-

"""
有向无环图（DAG）才有拓扑排序，非DAG图没有拓扑排序一说。
判断是否能够找到一个拓扑排序，本质上就是根据有向图的遍历判断是否有环。
而如果是想要找到一个拓扑排序，需要根据入度这个概念来处理。
或者，如果是找到单一source的有向图的拓扑排序（即单一连通分量），本质上是遍历，因为此时除了source没有入度为0的节点
https://songlee24.github.io/2015/05/07/topological-sorting/
"""
from collections import defaultdict, deque


def course_schedule(n, prerequisites):
    """
    https://leetcode.com/problems/course-schedule/description/
    总共n门课程，有一些课程需要先修课，比如[c1, c2]表示，c2是c1的先修课
    给定所有可能的先修课程关系array，判断是否能够完成n门课程
    其实就是遍历Graph的节点，然后判断是否有环，但此时是有向图，因为先修关系是有方向的edge[0] <- edge[1]
    这道题目的关键点就是，需要记录那些已经被遍历过得node，不然会有大量的重复遍历
    每个node会有三种状态  1）还没有被访问，表示0
                        2）正在被访问，用-1表示，也就是如果从某个source开始，重复访问了同一个节点，表明有环
                        3）之前已经在访问另一个source的时候，访问过了这个节点，用1表示，此时不再用考虑这个节点了
    时间空间复杂度均为 O(V+E)
    """
    def dfs(graph, visited, course_id):
        if visited[course_id] == -1:
            return False
        if visited[course_id] == 1:
            return True
        visited[course_id] = -1 # 即当前course正在被访问中
        adj_list = graph[course_id]
        for adj_course_id in adj_list:
            if not dfs(graph, visited, int(adj_course_id)):
                return False
        visited[course_id] = 1 # 即当前course已经被访问过了
        return True

    # 这里 adj list代表对于某个课程，它是哪些课程的先修课
    # 因为在graph中，如果a是b的先修课，那么a->b，即a指向b，所以需要从a访问到b
    graph = [[] for _ in xrange(n)]
    visited = [0 for _ in xrange(n)]
    # 首先，把edge list转换为adj list
    for c1, c2 in prerequisites:
        # c2 is a preq of c1
        graph[c1].append(c2)
    for course_id in xrange(n):
        if not dfs(graph, visited, course_id):
            return False
    return True


def course_schedule_order(n, prerequisites):
    """
    https://leetcode.com/problems/course-schedule-ii/description/
    类似上边的题，这里要返回的是，可能的一种选课的顺序，如果不能完成，返回一个空的list即可。
    这道题目跟alien dictionary区别是，这个可以是多个source，而那道题是单个source
    关键点是每次需要找到入度为0的节点，把它放到order里面之前，需要对于这个节点的相邻节点，更新他们的入度-1
    """
    graph = defaultdict(list)
    for c1, c2 in prerequisites:
        # c2 -> c1
        graph[c2].append(c1)
    in_degree_map = defaultdict(int)
    # 更新每个course的入度，即根据c2->c1来更新c1的入度
    for course_id, adj_list in graph.items():
        for adj_id in adj_list:
            in_degree_map[adj_id] += 1
    # 并把入度为0的course node加入到queue里面
    zero_queue = deque([])
    for course_id in xrange(n):
        # 入度为0，即不在in degree map里面
        if course_id not in in_degree_map:
            zero_queue.append(course_id)
    # 开始找order
    order = list([])
    while zero_queue:
        course_id = zero_queue.popleft()
        adj_list = graph[course_id]
        for adj in adj_list:
            # 更新这些相邻节点的入度
            in_degree_map[adj] -= 1
            if in_degree_map[adj] == 0:
                zero_queue.append(adj)
        # 对于当前入度为0的course节点，已经遍历完了它的所有相邻节点（即更新入度），把它放到order的下一个里
        order.append(course_id)
    return order if len(order) == n else []


def test():
    data = [(2, [[1, 0],[0,1]]),
            (3, [[1, 0], [2, 0], [1, 2]]),
            (4, [[1, 0], [2, 0], [1, 2], [3, 1]]),
            (4, [[1, 0], [2, 0], [1, 2], [3, 1], [0, 3]])
            ]
    for n, preq in data:
        print course_schedule_order(n, preq)


def alien_dictionary(words):
    """
    https://leetcode.com/problems/alien-dictionary/description/
    给定一组单词，已经按照外星人的规则排序好的，求出这个外星人词典的字母顺序
    比如["wrt","wrf","er","ett","rftt"] => 那么字母顺序就是 "wertf"
    可能会有多个结果，即有几个字母的顺序无法决定（同一层），那么返回其中一个可能结果即可。如果有环，则返回 empty string
    1. 根据输入的word，创建graph；
    2. DFS or BFS，找到topological顺序
    这道题目只存在一个联通分量，也就是整个图，因为给的input是word list，每个char都是存在于graph里面的
    而且这道题目是single source，也就是第一个word的第一个letter
    本道题目的关键点就是：1. 如何建graph 2. node有三种状态 3. 最后生成的order是逆序的，DFS走到了尽头，即顺序最小的node
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
        # 当前node visiting结束，加入到visited，同时，把对应的node放入到order中去
        visiting.remove(node)
        visited.add(node)
        order.append(node)

    # build adj list graph，这里面key node = 字母，value 就是 adj list，这里的adj是direct adj
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


def sequence_reconstruction(org, seqs):
    """
    https://leetcode.com/problems/sequence-reconstruction/description/
    给定一个original sequence，是一个1到n之间的某种排列关系
    判断是否能够根据seqs里面的pair关系，来建立出一个且唯一一个sequence
    如果这个sequence和original相同，返回True，否则False。
    本质上是拓扑排序找某一种可能，难点是如果判断这一种可能是唯一的？
    """
