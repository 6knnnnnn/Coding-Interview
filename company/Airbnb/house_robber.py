# -*- coding: utf-8 -*-
"""
Provide a set of positive integers (an array of integers).
Each integer represents numbers of nights user request on Airbnb.com.
If you are a host, you need to design and implement an algorithm to find out
the maximum numbers of nights you can accommodate.
The constrain is that you have to reserve at least one day between each request,
so that you have time to clean the room.

还是类似于house robber，只不过这里面每个request对应每个house，里面的request days对应house money


[3, 4, 5, 1, 9, 2, 1, 3]
"""


def house_robber_liner(house_money):
    """
    一排房子，里面有不同的钱，入室抢劫拿到尽可能多的钱，限制条件是，不能连续进入两间房间，否则警报会响
    DP[X] 到当前house X为止最大的抢劫钱数，是一个一维数组，最小值0，从左向右遍历
    初始化：DP[0]=money0, DP[1]=max(money0, money1)，状态转移：DP[X] = max( DP[X-2] + money[x], DP[X-1] )
    可以压缩空间为两个变量，分别记录DP[X-2] DP[X-1]
    Test case: [0], [0,0,0], [1,2], [1,2,1], [2,5,4], [2,3,0], [1,2,3,4,5,6,7]
    """
    if not house_money:
        return 0, []
    if len(house_money) == 1:
        return house_money[0], [0]
    # dp[0] = money[0]
    dp = house_money[:]
    # prev index用来记录，在我们遍历house money的时候，对于index k，之前是抢了哪一个house的
    prev_index = [-1] * len(house_money)
    prev_index[0] = 0
    dp[1] = house_money[0]
    if house_money[0] <= house_money[1]:
        # 从第二个开始抢，那么prev_index[1]变为1，代表需要从这个开始
        dp[1] = house_money[1]
        prev_index[1] = 1
    # 开始遍历house money
    for k in xrange(2, len(house_money)):
        rob_curr_money = house_money[k] + dp[k-2]
        if rob_curr_money > dp[k-1]:
            # 此时说明，对于当前house k来说，这次应该抢得是k和k-2
            # 所以prev index需要更新，即对于k，之前是抢了k-2的
            dp[k] = rob_curr_money
            prev_index[k] = k - 2
        else:
            # 此时说明，对于当前house k来说，这次应该抢得是k-1以及它之前的值，而非 k and k-2
            dp[k] = dp[k-1]
    i = len(house_money) - 1
    path = []
    while prev_index[i] != i:
        # 当i到达0或者1的时候，需要退出while loop，因为我们初始化prev_index[0]=0, prev_index[1] = 1 or -1
        # 到0的时候一定会退出，到1的时候可能会退出
        if prev_index[i] == -1:
            # prev_index[2:] 最开始初始化为-1
            # 如果没有被改变（即对应的house没有被抢劫），肯定还是-1，此时需要向后挪动i
            i -= 1
        else:
            # 如果prev_index[i] != i，而且prev_index[i] != -1，即被改变过，意味着i是被选中的house k，放到结果里
            # 同时，因为k-2也是被选中的house，所以i更新为prev_index[i]，也就是k-2
            path.append(i)
            i = prev_index[i]
    # while退出，此时i只可能是0或者1，对于其他的i>=2，不会存在prev_index[i] == i的情况
    path.append(i)

    return dp[-1], path

h = [1,2,3,4,5,6,7,8]

money, res = house_robber_liner(h)
print money
print res
