# -*- coding: utf-8 -*-


def island_perimeter(matrix):
    # https://leetcode.com/problems/island-perimeter/description/
    # 没有lake的情况，也就是里面不会有空点（其实有lake也没所谓？）
    # 简单的数学公式：岛屿的数量*4 - 相邻数量*2
    # 每一个岛屿为总周长贡献了4，而每两个相邻的岛屿又让总周长减少了2
    # 比如两个岛屿总周长8但是如果相邻，每个岛屿的一条边被合并了，总共为6
    # 所以遍历一遍矩阵，每次遇见一个岛屿，找他的下边和右边的相邻岛屿数量即可（如果有的话）
    # 时间复杂度 O(M*N)
    islands = neighbors = 0
    row, col = len(matrix), len(matrix[0])
    for i in xrange(row):
        for j in xrange(col):
            if matrix[i][j] == 1:
                islands += 1
                if i < row - 1 and matrix[i + 1][j] == 1:
                    neighbors += 1
                if j < col - 1 and matrix[i][j + 1] == 1:
                    neighbors += 1
    return islands * 4 - neighbors * 2

