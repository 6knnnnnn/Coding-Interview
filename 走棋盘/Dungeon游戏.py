# -*- coding: utf-8 -*-

"""
-2 (7=min(6,5)+2)	-3 (5=min(12,2)+3)	    3 (2)
-5 (6=min(1,12)+5)	-10 (12=min(5,1)+11)	1 (5)
10 (1)	            30 (1)	                -5 (6)
"""


def dungeon_game(matrix):
    """
    https://leetcode.com/problems/dungeon-game/description/
    Dungeon游戏，加血或者扣血
    代表意义：到达当前DP[X][Y]所需要的最少hp血量
    维度值域：原始输入一致，最小值为1
    初始化：最低行和最右列
    遍历方向：BR->LT逆向
    状态转移：DP[X][Y]从[X+1][Y] 和 [X][Y+1]中找最小，以及输入中[X][Y]的正负来判断
            为负则1-负数（要扣血），否则1（加血站只要最低血量到达就可以了）
    空间优化：滚动数组
    复杂度：O(N^2)
    """
    M, N = len(matrix), len(matrix[0])
    dp = matrix[:]  # copy from input
    for i in xrange(M - 1, -1, -1):
        for j in xrange(N - 1, -1, -1):
            daemon = matrix[i][j]
            # 下边的均为某个值减去daemon，如果daemon为负，结果为需要的最低血量
            if i == M - 1 and j == N - 1:  # last point
                dp[i][j] = max(1 - daemon, 1)
            elif i == M - 1:  # last row
                dp[i][j] = max(dp[i][j + 1] - daemon, 1)
            elif j == N - 1:  # last col
                dp[i][j] = max(dp[i + 1][j] - daemon, 1)
            else:  # in middle
                min_hp_next = min(dp[i + 1][j], dp[i][j + 1])
                dp[i][j] = max(1, min_hp_next - daemon)
    return dp[0][0]
