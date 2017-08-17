# -*- coding: utf-8 -*-

# sub array必须是连续的
# 关键点就在于，对于每一个nums[i]，判断之前subproblem的最大和子数组是否为正，如果为正，对当前i位置的problem的解有帮助
# 也就是，如果dp[i-1]为正，能够让dp[i]变大，那么更新dp[i]=dp[i-1]+nums[i]
# 否则，如果dp[i-1]为负，nums[i]不需要+dp[i-1]，dp[i]即为nums[i]


def maximum_sum_sub_array_dp(nums):
    # nums: [-2,1,-3,4,-1,2,1,-5,4]
    # DP:   [-2,1,-3,4, 3,5,6, 1,5]
    # dp[i]就是以i为结尾的subarray中最大和
    # dp[i]和子问题dp[i-1]依赖关系为
    # 若dp[i-1]>0，则dp[i]需要加上dp[i-1]，即之前子数组的解对当前问题的解有帮助（增加了sum）
    # 否则，dp[i]就是对应的nums[i]的值，不需要加dp[i-1]因为只会帮倒忙
    # 最后的结果是dp中最大的值
    dp = nums[:]  # 初始值为nums[i]自己
    for i in xrange(1, len(nums)):
        dp[i] += dp[i - 1] if dp[i - 1] > 0 else 0
    return max(dp)  # 若nums只有一个，就是nums[0]


# Kadane算法扫描一次整个数列的所有数值，在每一个扫描点计算以该点数值为结束点的子数列的最大和
# 该子数列有可能为空，或者由两部分组成：以前一个位置为结束点的最大子数列、该位置的数值
# Simple idea of the Kadane's algorithm is to look for all positive contiguous segments of the array
# (max_ending_here is used for this). And keep track of maximum sum contiguous segment among all positive segments
# (max_so_far is used for this). Each time we get a positive sum compare it with max_so_far and update max_so_far
# if it is greater than max_so_far
def maximum_sum_sub_array_kadane_index(nums):
    # Kadane算法，返回开始和结束index的情况
    max_temp = max_final = 0
    # Need to record the index of start and end of the maximum sum subarray
    start_final = start_temp = 0
    end_final = -1
    # nums:     [-2,1,-3,4,-1,2,1,-5,4]
    # max_temp   -2 1 -2 4  3 5 6  1 5
    # max_final  -2 1  1 4  4 5 6  6 6
    for i in xrange(0, len(nums)):
        max_temp = max_temp + nums[i]
        if max_temp < 0:
            max_temp = 0
            start_temp = i+1
        if max_final < max_temp:
            max_final = max_temp
            start_final = start_temp
            end_final = i # update end, so won't be -1 if there is any positive number
    if end_final == -1:
        # end_final init as -1 so to indicate all numbers are negative
        start_final = 0
        for i in xrange(len(nums)):
            # in this case find the maximum negative number (abs value the smallest) and its index
            if nums[i] > max_final:
                max_final = nums[i]
                start_final = end_final = i
    # return the max sum, and its starting and ending index
    return max_final, start_final, end_final

