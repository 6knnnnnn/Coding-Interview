# -*- coding: utf-8 -*-


def coin_change_min_coins_dp(coins, target):
    """
    https://leetcode.com/problems/coin-change/description/
    DP为target长度的一维数组，最小为0（不可换）
    DP[X]代表目标钱数为X时，根据已有的coins种类，最小换钱数，DP[0] = 0 即目标为0则一张都不用换，也就是换钱方法数只有一种
    对于每一个X，遍历所有货币coin求出剩余目标钱数remain
    若剩余钱数>=0，而且存在换钱的可能性（比如不是极值），找到min(DP[X], DP[remain]+1)，DP[remain]+1因为多了一个货币数
    时间复杂度 O(target * N)，空间复杂度O(target)
    """
    if target < 0: return -1
    if target == 0: return 0
    # dp[i]代表目标钱数为i的时候，最小的换钱数
    max_coins = target+1 # 不可能的换钱数
    dp = [0] * max_coins # 初始dp[0]=0 即一张都不用换
    for i in xrange(1, target+1): # 换钱数从1到target
        dp[i] = max_coins # 代表换钱数不存在（无法换）
        for coin in coins: # 遍历每一个coin的数值
            remain = i - coin # 剩余钱数至少要>=0
            if remain >= 0 and dp[remain] != max_coins:
                # 存在换的可能，则为具体的更小的换钱数目
                dp[i] = min(dp[remain]+1, dp[i])
    # -1表示不存在换钱数
    return dp[-1] if dp[-1] != max_coins else -1


def coin_change_min_coins_backtracking(coins, target):
    # 用一个map记录已知的目标钱数->最小换钱数，DFS的时候，如果有记录，直接返回，否则需要计算
    # 因为用到递归，recursion tree的高度为target，每一个node有coins个子节点
    # 时间空间和DP的一样，因为省去了所有重复计算
    # https://leetcode.com/articles/coin-change/
    def dfs_backtracking(coins, target, cache):
        if target < 0: return -1 # 不存在还钱的可能
        if target == 0: return 0 # 没有必要找，返回0
        if target in cache: return cache[target] # 历史记录
        total = target + 1
        for coin in coins:
            # DFS 找到下一个remain所对应的最小换钱数
            next_total = dfs_backtracking(coins, target-coin, cache)
            if next_total >= 0: # 存在还钱的可能，否则-1肯定是min，不能考虑进去
                total = min(next_total+1, total)
        # X=target+1没有被改变过，不存在可能
        cache[target] = -1 if total == target + 1 else total
        return cache[target]
    cache = {}
    return dfs_backtracking(coins, target, cache)


def coin_change_all_possible(coins, target):
    # 此时需要求得是，所有可能的换钱组合，需要一个DP[coins][target] table
    return


def perfect_squares(num):
    # https://leetcode.com/problems/perfect-squares/description/
    # 给定一个正整数num，从所有比num小的平方数中，找到和为num的组合的最小个数
    # 本质上是对于不同币种，即1, 4, 9, 16...的找零钱问题
    # 不同的是，肯定有一中还钱方法，因为有1存在，最不济num/1就是最后结果
    if num < 1:
        return 0
    coins = [i**2 for i in xrange(1, int(num**0.5)+1)]
    return coin_change_min_coins_dp(coins, num)
