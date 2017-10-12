# -*- coding: utf-8 -*-


def product_of_array_except_itself(nums):
    """
    https://leetcode.com/problems/product-of-array-except-self/description/
    可以用数组预处理的方式来计算，也可以节省空间，第一轮处理
         p:  1  n1  n1n2    n1n2n3
    output:  1  n1  n1n2    n1n2n3
    第二轮，逆序遍历
    output:  1       n1     n1n2    n1n2n3
         p:  n2n3n4  n3n4   n4      1
    output:  n2n3n4  n1n3n4 n1n2n4  n1n2n3
    """
    p = 1
    output = []
    for i in xrange(0, len(nums)):
        output.append(p)
        p = p * nums[i]
    p = 1
    for i in xrange(len(nums)-1,-1,-1):
        output[i] = output[i] * p
        p = p * nums[i]
    return output


def maximum_product_subarray(nums):
    """
    https://leetcode.com/problems/maximum-product-subarray/description/
    DP[X]代表在X位置时，子数组[0...x] 中乘积的最大值和最小值
    DP是一维数组 所有整数
    DP初始化就是原始输入数组的copy（或者两个变量，空间压缩）
    遍历方向L->R
    状态转移：若input[X]为负，则将DP[X-1]的maxp和minp交换。DP[X]的maxp和minp就等于他们分别和input[X]相乘后，
            跟input[X]相比的最大（小）值，需要跟input[X]比较因为可能为负
    空间压缩：单一变量	O(N)
    """
    if not nums:
        return 0
    # 正（负）找之前的最大（小）值
    max_p, min_p = nums[0], nums[0]
    res = nums[0]
    for n in nums[1:]:
        if n < 0:  # 此时为负值，交换
            max_p, min_p = min_p, max_p
        max_p = max(n, max_p * n)
        min_p = min(n, min_p * n)
        res = max(res, max_p)
    return res
