from collections import defaultdict, deque


def alien_dictionary_bfs(words):
    # build graph by edges
    graph = {node: [] for node in set(''.join(words))}
    for i, w1 in enumerate(words[:-1]):
        for j in xrange(i + 1, len(words)):
            w2 = words[j]
            for k in xrange(min(len(w1), len(w2))):
                c1, c2 = w1[k], w2[k]
                if c1 != c2:
                    graph[c1].add(c2)
                    break
    # build in-degree map
    in_degree_map = defaultdict(int)
    for node, adj_list in graph.items():
        for adj_node in adj_list:
            in_degree_map[adj_node] += 1
    # put 0-in-degree node to queue
    zero_queue = deque([])
    for node in graph.keys():
        if node not in in_degree_map:
            zero_queue.append(node)
    # iterate each node in queue, update in-degree and order
    order = list([])
    while zero_queue:
        node = zero_queue.popleft()
        order.append(node)
        adj_list = graph[node]
        for adj in adj_list:
            in_degree_map[adj] -= 1
            if in_degree_map[adj] == 0:
                zero_queue.append(adj)
                in_degree_map.pop(adj)
    # return order, if in-degree-map not empty, cricle
    return "".join(order) if len(in_degree_map) == 0 else ""
