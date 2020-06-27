# -*- coding: utf-8 -*-
# 本质上都是费布那齐数列问题，即F(X) = F(X-a) + F(X-b)


def house_robber_liner(houses):
    """
    https://leetcode.com/problems/house-robber/description/
    一排房子，里面有不同的钱，入室抢劫拿到尽可能多的钱，限制条件是，不能连续进入两间房间，否则警报会响
    DP[X] 到当前house X为止最大的抢劫钱数，是一个一维数组，最小值0，从左向右遍历
    初始化：DP[0]=money0, DP[1]=max(money0, money1)，状态转移：DP[X] = max(DP[X-2] + money[x], DP[X-1])
    可以压缩空间为两个变量，分别记录DP[X-2] DP[X-1]
    Test case: [0], [0,0,0], [1,2], [1,2,1], [2,5,4], [2,3,0], [1,2,3,4,5,6,7]
    """
    def dp_array_space(house_money):
        if not house_money:
            return 0
        if len(house_money) == 1:
            return house_money[0]
        dp = house_money[:] # dp[0] = money[0]
        dp[1] = max(house_money[0], house_money[1])
        for k in xrange(2, len(house_money)):
            dp[k] = dp[k - 1]
            if dp[k-2] + house_money[k] > dp[k-1]:
                dp[k] = dp[k - 2] + house_money[k]
        return dp[-1]

    def dp_2_variables(house_money):
        k2 = k1 = 0
        for m in house_money:
            k2, k1 = k1, max(k1, k2 + m)
        return k1

    def dp_index(house_money):
        # 此题目难点是如何记录index？
        # 初始化为长度为总house数目的-1数组，相当于是一个flag，表示如果对应的i位置的house被抢劫了
        # 则这个数组的i位置的值就是i本身，否则为-1代表这个house被忽略了
        if not house_money:
            return 0, []
        if len(house_money) == 1:
            return house_money[0], [0]
        dp = house_money[:] # dp[0] = money[0]
        prev = [-1] * len(house_money)
        prev[0] = 0
        if house_money[0] <= house_money[1]:
            dp[1] = house_money[1]
            prev[1] = 1

        for k in xrange(2, len(house_money)):
            dp[k] = dp[k - 1]
            if dp[k-2] + house_money[k] > dp[k-1]:
                dp[k] = dp[k - 2] + house_money[k]
                prev[k] = k - 2
        return dp[-1], prev

    v1, index = dp_index(houses)
    print houses, v1, index
    i = len(index) - 1
    res_index = []
    while index[i] != i:
        if index[i] == -1:
            i -= 1
        else:
            res_index.append(i)
            i = index[i]
            if i == 0 or i == 1:
                res_index.append(i)
                break
    print res_index



samples = [
    [2,1,1,1], [2,3,0],
    [0], [0,0,0], [1,2], [1,2,1], [2,5,4], [2,3,0], [1,2,3,4,5,6,7]
]
for s in samples:
    house_robber_liner(s)


def house_robber_liner_circular(houses):
    """
    https://leetcode.com/problems/house-robber-ii/description/
    跟上边的规则一样，只是头尾可以相连，也就是不能进入头部的同时，又进入尾部
    DP分割问题，依赖关系不变，但是分两种情况：1）从第一个房子开始打劫，到倒数第二个为止 2） 从第二个房子开始，到最后一个
    这两种情况互斥，因为打劫了第一个，那么最后一个就不能再打劫了
    """
    def rob_range(houses_money, i, j):
        k1 = k2 = 0
        for money in houses_money[i:j + 1]:
            k2, k1 = k1, max(k2 + money, k1)
        return k1

    if not houses:
        return 0
    if len(houses) == 1:
        return houses[0]
    start_1st = rob_range(houses, 0, len(houses) - 2)
    start_2nd = rob_range(houses, 1, len(houses) - 1)
    return max(start_1st, start_2nd)


def house_robber_binary_tree(houses_tree):
    """
    https://leetcode.com/problems/house-robber-iii/description/
    警报响起的条件仍旧是访问相邻的house，只不过此时"相邻"意味着，parent-child的相邻关系
    DP[X]：从二叉树的叶节点开始，"自顶向上"到目前节点house X为止最大的抢劫钱数
    所以需要DFS到最底层，每次DFS返回的是K1 K2，最底层返回的是K1 = K2 = 0
    对于root即DP[X]，此时的DP[X-1]代表root的左+右孩子的和，DP[X-2]代表root的左+右孩子各自的孩子的最优解
    而root的值，就是对应的最新的house money，更新方式一致
    """
    def dfs(parent):
        k2 = k1 = 0
        if parent:
            left_dp, right_dp = dfs(parent.left), dfs(parent.right)
            # k2, k1 = k1, max(k1, k2+money)
            k1, k2 = left_dp[0] + right_dp[0], left_dp[1] + right_dp[1]
            k2, k1 = k1, max(k1, k2 + parent.val)
        return k1, k2
    #  返回K1
    return dfs(houses_tree)
