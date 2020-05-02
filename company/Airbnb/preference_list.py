# -*- coding: utf-8 -*-
"""
  每个人都有一个preference的排序，在不违反每个人的preference的情况下得到总体的preference的排序

  For example:
  a: 2, 3, 5
  b: 4, 2, 1
  c: 4, 1, 5, 6
  d: 4, 7

  Return:
  4, 2, 7, 3, 1, 5, 6

  拓扑排序解决
  (follow up break tie with person1)
"""
from collections import defaultdict, deque


def preference_list(preferences):
    # 1. build graph，假设输入是key->list pair
    graph = defaultdict(list)
    for pre_list in preferences.values():
        for i in xrange(len(pre_list)-1):
            n1, n2 = pre_list[i], pre_list[i+1]
            graph[n1].add(n2)
    # 2. build in-degree-map
    in_degree_map = defaultdict(int)
    for node, adj_list in graph.items():
        for adj in adj_list:
            in_degree_map[adj] += 1
    # 3. find zero-in-degree node, put into queue
    zero_queue = deque([])
    for node in graph.keys():
        if node not in in_degree_map:
            zero_queue.append(node)
    # 4. iterate each node in queue, update in-degree and order
    order = list([])
    while zero_queue:
        node = zero_queue.popleft()
        order.append(node)
        for adj in graph[node]:
            in_degree_map[adj] -= 1
            if in_degree_map[adj] == 0:
                zero_queue.append(adj)
                in_degree_map.pop(adj)
    # 5. return result order
    return order if len(in_degree_map) == 0 else []

pre_dict = {
    "a": [2, 3, 5], "b": [4, 2, 1], "c": [4, 1, 5, 6], "d": [4, 7]
}

result = preference_list(pre_dict)

print result
