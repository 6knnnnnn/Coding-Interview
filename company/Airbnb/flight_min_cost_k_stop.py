# -*- coding: utf-8 -*-
"""
 * 给一些edge和cost，指定起始点和终点，找最多stop k次的最便宜的价格
 * A->B,100,
 * B->C,100,
 * A->C,500.
 * 如果k是1的话，起点终点是A，C的话，那A->B->C的cost最小是200
 *
 * 本质是BFS一层层往外搜，可以把从起点到当前node的最小值存在这个node中，可以用来加速剪枝
 * follow up可以是输出路线，需要保存parent信息

1. build graph
2. BFS traversal find the min cost
"""
import sys
from collections import deque


class Node(object):
    def __init__(self, name):
        self.name = name
        # 这里面min cost记录的是，从source到达这个node，所花费的最小cost
        self.min_cost_from_source = sys.maxint
        # key = adj node, value = cost from the source -> self -> adj node
        self.adj_nodes_cost = dict([])

    def __repr__(self):
        return "%s: %s adjs, cost=%s" % (self.name, len(self.adj_nodes_cost), self.min_cost_from_source if self.min_cost_from_source != sys.maxint else -1)


def bfs(source, target, k, parent):
    reach_target = False
    # queue里面记录的是，从source开始到达这个node的时候，所花费的全局最小成本是多少
    # 刚开始的时候是0，即从source到source肯定是0
    node_queue = deque([(source, 0)])
    stop = -1
    while node_queue and stop <= k:
        stop += 1
        size = len(node_queue)
        # BFS queue 按层来遍历
        for _ in xrange(size):
            curr_node, min_cost_so_far = node_queue.popleft()
            curr_node.min_cost = min(min_cost_so_far, curr_node.min_cost)
            if curr_node.name == target.name:
                # 此时虽然到达了target，但是还是需要继续检查其他的可能路径，因为并不一定此时是最优解
                # 所以还需要继续到该层的下一个node
                reach_target = True
            else:
                for adj_node, adj_cost in curr_node.adj_nodes_cost.items():
                    # new cost即代表，从source到当前的curr node位置的最小cost
                    # 再加上adj cost，即等于从source到curr node再到adj node的最小cost
                    new_cost = min_cost_so_far + adj_cost
                    if new_cost < adj_node.min_cost and \
                        (stop < k or stop == k and adj_node.name == target):
                        # 如果是一个更小的cost，需要记录parent关系，并且加入到下一层的queue中
                        parent[adj_node.name] = curr_node.name
                        node_queue.append((adj_node, new_cost))
    return reach_target


def find_min_cost_plan(lines, source, target, k):
    # 1. build graph by lines
    graph = dict([])
    for line in lines:
        first = line.split(",")
        second = first[0].split("->")
        n1, n2 = second[0], second[1]
        cost = first[1]
        if n1 not in graph:
            graph[n1] = Node(n1)
        if n2 not in graph:
            graph[n2] = Node(n2)
        n1 = graph.get(n1)
        n2 = graph.get(n2)
        n1.adj_nodes_cost[n2] = int(cost)
    # 2. BFS each node, and also build a parent-child map
    parent = dict([])
    reach_target = bfs(graph[source], graph[target], k, parent)
    path = list([])
    result = -1
    # 3. if reach to the target, recover the path by the parent-child map
    if reach_target:
        result = graph[target].min_cost
        node = target
        while node != source:
            path.append(node)
            node = parent[node]
        path.append(source)
    return result, path[::-1]


lines = [
    "A->B,100", "A->C,500", "B->C,100"
    , "A->D,10","D->C,10",
    # "A->B,100","A->B,100","A->B,100","A->B,100","A->B,100",
    # "A->B,100","A->B,100"
]

source, target = "A", "C"
k = 3

print find_min_cost_plan(lines, source, target, k)






