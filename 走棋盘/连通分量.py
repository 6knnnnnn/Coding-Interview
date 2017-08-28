# -*- coding: utf-8 -*-

# 用"注水sink"的方式，把已经遍历过得cell标记，但标记之后什么逻辑处理要看题意
# DFS + BFS

from collections import deque


def number_islands(matrix):
    # https://leetcode.com/problems/number-of-islands/description/
    # 用一个DFS方法，因为只是01 cell，把所有遍历过的1变成别的flag比如2
    # 这样之后还可以把输入matrix还原。如果是变成0，无法还原
    def sink(lands, i, j):
        if 0 <= i < len(lands) and 0 <= j < len(lands[0]) and lands[i][j] == '1':
            lands[i][j] = '2'
            for k in [(i+1, j),(i-1, j), (i, j+1), (i, j-1)]:
                sink(lands, k[0], k[1])
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


def surrounded_regions(board):
    """
    https://leetcode.com/problems/surrounded-regions/description/
    把所有被X上下左右包围的O区域换为X，如果是联通了边界的O区域，不需要换X（下图情况2）
    X X X X     X X X X    X X X X     X X X X
    X O O X ->  X X X X    X O X X ->  X X X X
    X X O X     X X X X    X X O X     X X O X
    X O X X     X O X X    X O O X     X O O X
    这道题目用BFS和DFS均可做。时间复杂度O(M*N)，空间复杂度最坏情况O(M*N)，即全部都是O
    从四条边上的O开始找起，所有和这些O相联通的O都改变为W（相当于注水Water）
    之后遍历所有cell，对于没有改变为W的O均变为X，W的均变为O，也就还原了最后的答案
    """
    def sink(board, i, j, m, n):
        if 0 <= i < m and 0 <= j < n:
            if board[i][j] == 'O':
                board[i][j] = 'W'
            # 上下左右依次注水，此时需要注意的是，不能重复的访问边界，特别是上边界
            # 即，i-1>0 i+1<m-1 j-1>0 j+1<n-1
            for r, c in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 < r < m and 0 < c < n and board[r][c] == 'O':
                    sink(board, r, c, m, n)
    if board:
        # 至少是一个3X3的矩阵,2x2的矩阵不用变
        m, n = len(board), len(board[0])
        if m < 2 or n < 2:
            return
        # 所有在边界上的O都不会变成X，从这些边界开始
        # python string immutable，所以需要额外的空间来存储，最后改变board每一行
        # 除非输入是一个list of list，即每一行里面的元素为list of char
        board_copy = [list(row) for row in board ]
        for i in xrange(m):
            if board_copy[i][0] == 'O':
                sink(board_copy, i, 0, m, n)
            if board_copy[i][n-1] == 'O':
                sink(board_copy, i, n-1, m, n)
        for j in xrange(n):
            if board_copy[0][j] == 'O':
                sink(board_copy, 0, j, m, n)
            if board_copy[m-1][j] == 'O':
                sink(board_copy, m-1, j, m, n)
        # 4个边界处理完成，还原board，O变成X，W变成O
        for i in xrange(m):
            for j in xrange(n):
                if board_copy[i][j] == 'O':
                    board_copy[i][j] = 'X'
                elif board_copy[i][j] == 'W':
                    board_copy[i][j] = 'O'
        for i in xrange(m):
            # 把copy的值复制到原始输入，inplace change
            board[i] = ''.join(board_copy[i])


def walls_and_gates_distance(rooms, inf=2147483647):
    """
    https://leetcode.com/problems/walls-and-gates/description/
    单源多终点，扩展到多源多终点，BFS
    """
    if not rooms:
        return
    m, n = len(rooms), len(rooms[0])
    # 一个queue，记录所有可以到达exit出口的房间，初始化为所有为0的cell，即exit出口
    exit_queue = deque([])
    for i in xrange(m):
        for j in xrange(n):
            if rooms[i][j] == 0:
                exit_queue.append((i, j))
    while exit_queue:
        # 找到所有可以exit的房间，并且更新他们的距离
        i, j = exit_queue.popleft()
        for r, c in [(i+1, j), (i-1, j), (i, j+1),(i, j-1)]:
            if 0 <= r < m and 0 <= c < n and rooms[r][c] == inf:
                # 这里面只更新一次INF，即第一次遇到INF的时候，可以避免重复访问
                exit_queue.append((r, c))
                # 更新room i j 的上下左右四个方向的到达exit的距离
                rooms[r][c] = rooms[i][j] + 1
    return rooms


b = [[2147483647,-1,0,2147483647],
     [2147483647,2147483647,2147483647,-1],
     [2147483647,-1,2147483647,-1],
     [0,-1,2147483647,2147483647]]

print walls_and_gates_distance(b)
