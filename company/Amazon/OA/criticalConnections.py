def help(edges, vRemoved, totalVeticesNum):
    history = set([])

    for edge in edges:
        v1, v2 = edge[0], edge[1]
        # ignore the v to be removed
        if v1 == vRemoved or v2 == vRemoved:
            continue

        if len(history) == 0 or v1 in history or v2 in history:
            history.add(v1)
            history.add(v2)

    # if even after this v removed, all the other nodes could be visited in history
    # then this v is not a critical connection vertex
    return len(history) == totalVeticesNum - 1



from collections import defaultdict

def findCC(n, connections):
    graph = defaultdict(set)
    for v1, v2 in connections:
        graph[v2].add(v1)
        graph[v1].add(v2)

    jump = [-1] * n

    def dfs(v, parent, level, jump, result, graph):
            jump[v] = level + 1
            for child in graph[v]:
                if child == parent:
                    continue
                elif jump[child] == -1:
                    temp = dfs(child, v, level+1, jump, result, graph)
                    jump[v] = min(jump[v], temp)
                else:
                    jump[v] = min(jump[v], jump[child])

            if jump[v] == level + 1 and v != 0:
                res.append([parent, v])
            return jump[v]

    res = []
    dfs(0, -1, 0, jump, res, graph)
    return res