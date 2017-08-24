# -*- coding: utf-8 -*-


def number_islands(matrix):
    # https://leetcode.com/problems/number-of-islands/description/
    # 用一个DFS方法，因为只是01 cell，把所有遍历过的1变成别的flag比如2
    # 这样之后还可以把输入matrix还原。如果是变成0，无法还原
    def sink(lands, i, j):
        if 0<=i<len(lands) and 0<=j<len(lands[0]) and lands[i][j] == '1':
            lands[i][j] = '2'
            sink(lands, i + 1, j)
            sink(lands, i - 1, j)
            sink(lands, i, j + 1)
            sink(lands, i, j - 1)
    total = 0
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[i])):
            if matrix[i][j] == '1':
                # 找到一个新的岛屿，用DFS sink这个岛，之后不会再次遍历这个岛了，也就是total+1只出现一次
                sink(matrix, i, j)
                total += 1
    # 如果最后需要recover matrix，把所有2变为1
    return total


def number_islands_2(m, n, positions):
    # https://leetcode.com/problems/number-of-islands-ii/description/
    # 问题关键点是，如果新加入的1，能够让两个或者多个岛屿相连怎么办？并查集
    def new_island(matrix, i, j, m, n):
        for x, y in ((i+1,j), (i-1, j), (i, j+1), (i, j-1)):
            if 0<=x<m and 0<=y<n and matrix[x][y] == 1:
                return False
        return True

    matrix = [[0] * n for _ in xrange(m)]
    result = list([])
    curr = 0
    for pos in positions:
        i, j = pos[0], pos[1]
        matrix[i][j] = 1
        if new_island(matrix, i, j, m, n):
            curr += 1
        result.append(curr)
    return result

pos = [[0,0],[0,1],[1,2],[2,1]]
print number_islands_2(3, 3, pos)
