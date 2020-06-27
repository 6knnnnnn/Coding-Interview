# -*- coding: utf-8 -*-


def uniquePathCount(row, col):
    # https://leetcode.com/problems/unique-paths/
    # dp[i][j]: from start to i,j, max combinations
    dp = [[0 for _ in xrange(col)] for _ in xrange(row)]

    for r in xrange(row):
        for c in xrange(col):
            if r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = dp[r-1][c] + dp[r][c-1]

    return dp[-1][-1]


for r, c in [(3, 2), (7, 3)]:
    print r,c, uniquePathCount(r, c)


def uniquePathWithObstacles(grid):
    # https://leetcode.com/problems/unique-paths-ii/
    row, col = len(grid), len(grid[0])
    dp = [[0 for _ in xrange(col)] for _ in xrange(row)]

    # 初始化DP，根据grid对应位置是否有obstacle，以及上一个DP点是1还是0（0意味着之前有obstacle）
    dp[0][0] = 1 if grid[0][0] == 0 else 0
    for r in xrange(1, row):
        dp[r][0] = 1 if grid[r][0] == 0 and dp[r-1][0] == 1 else 0
    for c in xrange(1, col):
        dp[0][c] = 1 if grid[0][c] == 0 and dp[0][c-1] == 1 else 0

    for r in xrange(1, row):
        for c in xrange(1, col):
            # 根据对应位置的grid是否有obstacle来更新
            dp[r][c] = 0 if grid[r][c] == 1 else dp[r - 1][c] + dp[r][c - 1]

    return dp[-1][-1]


def uniquePathStartToEnd(grid):
    # https://leetcode.com/problems/unique-paths-iii
    pass

