# -*- coding: utf-8 -*-
# 关键点：不要遍历到之前已经遍历过得节点

from utility.entity import UndirectedGraphNode
from collections import deque, defaultdict


def clone_graph(original):
    """
    https://leetcode.com/problems/clone-graph/description/
    用一个map记录已经clone过了的node，如果存在，直接返回，否则从新创建一个node加入到map的同时
    clone这个node的所有相邻节点
    """
    def dfs(node, node_map):
        if not node:
            return
        if node.label in node_map:
            return node_map[node.label]
        clone = UndirectedGraphNode(node.label)
        node_map[clone.label] = clone
        for adj in node.neighbors:
            clone_adj = dfs(adj, node_map)
            node.neighbors.add(clone_adj)
        return clone

    # BFS, 类似于DFS，也是用map，不同的是，如果某个node不存在于map中，加入到待处理queue
    if not original:
        return None
    new_original = UndirectedGraphNode(original.label)
    clone_queue = deque([original]) # 从original开始处理
    cloned_map = {original.label: new_original}
    while clone_queue:
        node = clone_queue.popleft()
        for adj in node.neighbors:
            if adj.label not in cloned_map:
                # 还没有被克隆，把它加到queue里面之后需要克隆
                cloned_map[adj.label] = UndirectedGraphNode(adj.label)
                clone_queue.append(adj)
            adj_clone = cloned_map[adj.label]
            cloned_map[node.label].neighbors.add(adj_clone)
    return new_original


def graph_valid_tree(edges, n):
    """
    https://leetcode.com/problems/graph-valid-tree/description/
    Given n = 5 and edges = [[0, 1], [0, 2], [0, 3], [1, 4]], return true.
    Given n = 5 and edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], return false.
    判断一个graph是否是一个tree（不一定要二叉树），也就是判断是否有环+所有联通分量个数=1，（不相连就是forest了而非tree）
    本质上就是从某个source开始遍历graph，如果遍历完成后，没有环，以及没有不相连的部分，就代表是一个tree
    有点类似于number_of_connected_components_in_undirected_graph，但是需要两步骤：分别检查无环，和联通分量个数
    额外空间O(N)，时间O(E)
    """
    def has_cycle(graph, visited, curr_node, direct_parent):
        # 从当前节点开始，判断graph里面是否有环，direct source节点，即当前节点之前是作为哪个节点的adj访问过来的（直接相邻）
        visited.add(curr_node)
        for adj in graph[curr_node]:
            if adj in visited:
                if direct_parent != adj:
                    # 因为这里面是无向图，如果curr node的相邻节点adj被重复访问了，但adj的direct parent是adj自己，此时不算有环
                    # 比如 1 --- 2 --- 3 从1访问2的时候，2仍然会遍历回去1，但此时2的直接父节点是1，不算是有环
                    #       \_________/
                    # 而如果是从2遍历到3，3却遍历回到了1（已经在visited），1却不是3的直接parent，所以有环
                    return True
            elif has_cycle(graph, visited, adj, curr_node):
                # 判断从adj开始，是否有环
                return True
        return False

    # adj list represent a graph
    graph = defaultdict(list)
    for x, y in edges:
        graph[x].add(y)
        graph[y].add(x)
    visited = set([])
    # 先是遍历图，判断是否有环，同时更新visited hash set，之后
    # 如果没有任意的节点（0..n-1）没有被访问过，返回TRUE，也就是所有的node都在一个连通分量里面
    return not has_cycle(graph, visited, 0, -1) and not any(i not in visited for i in xrange(n))


def test_valid_graph_tree():
    input = [(7, [[0, 1], [0, 2], [2, 3], [2, 4], [5, 6]]), # 无环，但是有不相连的部分
             (7, [[0, 1], [0, 2], [2, 3], [2, 4], [5, 4], [5, 6]]), # True
             (5, [[0, 1], [0, 2], [2, 3], [2, 4]]),
             (3, [[0, 1], [0, 2],[2, 1]])
             ]
    for n, edges in input:
        print graph_valid_tree(edges, n)
