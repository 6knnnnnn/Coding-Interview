# -*- coding: utf-8 -*-

"""
 * Given a directed graph, find the minimal number of vertices that can traverse all the vertices from them.
 * For example
 * 2->3->1->2->0, 4->5
 * Then we need [1, 4] (or [2, 4], [3, 4]) to traverse all the vertices.
 * Only one solution is needed if there are more than one possibilities.

用一个hash set记录最后的结果res

对于每次从某个source开始的node，开始DFS，如果遇到了的节点x，已经在res里面了
说明我们可以从这个node遍历到x，x不需要在结果里面了

"""
from collections import defaultdict


def min_graph_traversal_nodes(edges):
    def dfs(res, graph, visited, visiting, current, source):
        adj_set = graph[current]
        for adj in adj_set:
            if adj in res and adj != source:
                # if same as source, a cycle, but still ok, keep it in res
                res.remove(adj)
            if adj not in visiting:
                visiting.add(adj)
                visited.add(adj)
                dfs(res, graph, visited, visiting, adj, source)

    # build graph with adj list
    graph = defaultdict(set)
    node_set = set([])
    for n1, n2 in edges:
        graph[n1].add(n2)
        node_set.add(n1)
        node_set.add(n2)
    # DFS to visit all nodes, and meanwhile change result set
    res, visited = set([]), set([])
    for n in node_set:
        if n not in visited:
            res.add(n)
            visited.add(n)
            # visiting: current connected component, visited: global visited records
            visiting = set([])
            dfs(res, graph, visited, visiting, n, n)
    return res
