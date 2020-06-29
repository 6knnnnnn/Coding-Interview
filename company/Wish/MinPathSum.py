# -*- coding: utf-8 -*-

class PathSum(object):
    def __init__(self, pathSum, row, col):
        self.pathSum = pathSum
        self.row = row
        self.col = col


def minimum_path(grid):
    # https://leetcode.com/problems/minimum-path-sum/
    dp = grid[:]
    for row in xrange(len(grid)):
        dp.append([])
        for col in xrange(len(grid[row])):
            if row == 0 and col == 0 or (row != 0 and col != 0):
                dp[row][col] = PathSum(grid[row][col], row, col)
            # 初始化第一列和第一行 非 0，0 moveToCell
            elif row == 0:
                dp[row][col] = PathSum(grid[row][col] + grid[row][col-1], 0, col-1)
            elif col == 0:
                dp[row][col] = PathSum(grid[row][col] + grid[row-1][col], row-1, col)

    # traverse the dp matrix
    for row in xrange(1, len(grid)):
        for col in xrange(1, len(grid[row])):
            prevCol, prevRow = dp[row][col-1], dp[row-1][col]
            if prevCol[0] > prevRow[0]:
                dp[row][col] = (dp[row][col] + prevRow[0], prevRow[1])
            else:
                dp[row][col] = (dp[row][col] + prevCol[0], prevCol[1])

    return dp[-1][-1]


def min_path_sum(grid):
    dp = grid[:]
    # 初始化第一列和第一行
    for col in xrange(1, len(grid[0])):
        dp[0][col] += dp[0][col - 1]
    for row in xrange(1, len(grid)):
        dp[row][0] += dp[row - 1][0]

    # traverse the grid
    for row in xrange(1, len(grid)):
        for col in xrange(1, len(grid[row])):
            dp[row][col] += min(dp[row][col - 1], dp[row - 1][col])

    return dp[-1][-1]


grid = [
  [1,3,1],
  [1,5,1],
  [4,2,1]
]

print min_path_sum(grid)
