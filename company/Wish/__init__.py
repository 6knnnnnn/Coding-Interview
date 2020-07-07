land = 1
water = 0


def numAdjEdges(matrix, i, j):
    if i == 1 and j == 1:
        a = 1
    edges = 0
    if matrix[i][j] == land:
        firstLastR = i in [0, len(matrix) - 1]
        firstLastC = j in [0, len(matrix[i]) - 1]
        if firstLastR and firstLastC:
            # on top/bottom left/right -> 2 edges at least + num of water
            edges = 2
        elif firstLastR or firstLastC:
            # on one edge only -> 1 edge at least + num of water
            edges = 1
        # num of water -> num of edges + num of water
        for k1, k2 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if 0 <= k1 < len(matrix) and 0 <= k2 < len(matrix[k1]) and matrix[k1][k2] == water:
                edges += 1
    print "---", i, j, edges
    return edges


def dfs(matrix, i, j, currIslandArea, currIslandPer):
    if 0 <= i < len(matrix) and 0 <= j < len(matrix[i]) and matrix[i][j] == land:
        currIslandArea[0] += 1
        currIslandPer[0] += numAdjEdges(matrix, i,
                                        j)  # calcualte the num of non-land edge adj to this cell
        matrix[i][j] = '#'
        for k in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            dfs(matrix, k[0], k[1], currIslandArea, currIslandPer)


def numOfIslands(matrix):
    """
    DFS -> change visited lands to placeholder
    """
    total = 0
    islandArea = []
    islandPer = []
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[i])):
            if matrix[i][j] == land:
                currIslandArea = [0]
                currIslandPer = [0]
                dfs(matrix, i, j, currIslandArea, currIslandPer)
                total += 1
                islandArea.append(currIslandArea[0])
                islandPer.append(currIslandPer[0])

    return total, islandArea, islandPer


inputs = [
    [1, 1, 1, 0, 0],
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1],
]

print numOfIslands(inputs)