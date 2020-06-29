# -*- coding: utf-8 -*-

"""
https://leetcode.com/problems/maximum-subarray/description

找到所有，累加和为正的连续子数组分区的和（sum of positive contiguous segments of the array），其中的最大值即为结果
关键点就在于，对于每一个nums[i]，判断之前subproblem的最大和子数组是否为正，如果为正，对当前i位置的problem的解有帮助
也就是，如果dp[i-1]为正，能够对dp[i]有帮助（变大），那么更新dp[i]=dp[i-1]+nums[i]
否则，如果dp[i-1]为负，只会帮倒忙，对dp[i]没有帮助，dp[i]即为nums[i]，无论nums[i]是正负，不需要加上dp[i-1]
"""


def maximum_sum_sub_array_dp(nums):
    # nums: [-2,1,-3,4,-1,2,1,-5,4]
    # DP:   [-2,1,-2,4, 3,5,6, 1,5]
    # dp[i]就是以i为结尾的子数组最大和，但最后结果不一定是最后一个n-1结尾，是藏在dp里面的某个值
    # 和子问题dp[i-1]依赖关系为：
    #   若dp[i-1]>0，则dp[i]需要加上dp[i-1]，即之前子数组的解对当前问题的解有帮助（增加了sum）
    #   否则，dp[i]就是对应的nums[i]的值，不需要加dp[i-1]因为只会帮倒忙
    # dp中存的只是以i结尾的子数组最大和，最后的结果是dp中最大的值
    dp = [0] * len(nums)
    dp[0] = nums[0] # 初始值为nums[0]
    for i in xrange(1, len(nums)):
        dp[i] = nums[i]
        if dp[i-1] > 0:
            dp[i] = nums[i] + dp[i - 1]
    # 若nums只有一个，就是nums[0]
    # 若nums均为负数，那么就是其中最大的
    # 如果是找到最后的index range，其实就是，dp里面max val的j，和之前的第一个负数的i：[i+1, j]
    return max(dp)


def maximum_sum_sub_array_kadane(nums):
    """
    Kadane算法扫描一次整个数列的所有数值，在每一个扫描点计算以该点数值为结束点的子数列的最大和
    当遍历到i位置的数字，max_temp等价于DP[i-1]
    max_temp>=0，因为记录的是，累加和为正的连续子数组分区的和，不可能为<0
    之后跟当前nums[i]相加，如果为正，说明当前n对累加和为正的连续子数组分区，有帮助，可以归到分区中
    否则，max_temp=0，此时这个分区结束了，需要寻找下一个分区。
    max_final用来记录目前为止所有，累加和为正的连续子数组分区的和的最大值，即最后结果
    nums:      [-2,1,-3,4,-1,2,1,-5,4]
    max_local  0, 0 1  0 4  3 5 6  1 5
    max_global 0, 0 1  1 4  4 5 6  6 6
    """
    max_local = max_global = 0
    for n in nums:
        max_local += n
        if max_local < 0:
            max_local = 0
        max_global = max(max_global, max_local)
    return max_global


def maximum_sum_sub_array_kadane_index(nums):
    # Kadane算法，返回开始和结束index的情况
    max_temp = max_final = 0
    # 找到对应子数组的开始和结束index
    start_final = start_temp = 0
    end_final = -1
    for i in xrange(0, len(nums)):
        max_temp += nums[i]
        if max_temp < 0:
            max_temp = 0
            # 此时说明之前的累加和为正的连续子数组分区结束了，需要找到一个新的，累加和为正的连续子数组分区
            start_temp = i+1
        if max_final < max_temp:
            # 如果当前的累加和为正的连续子数组分区的和比max_final要大
            # 更新max_final start_final end_final，即此时找到了新的分区
            max_final = max_temp
            start_final = start_temp
            end_final = i # update end, so won't be -1 if there is any positive numbers
    if end_final == -1:
        # 初始化为-1，如果遍历完整个数组后仍旧为负数，表明所有数字都是负数，所以找到数组中最大的index
        start_final = 0
        for i in xrange(len(nums)):
            if nums[i] > max_final:
                max_final = nums[i]
                start_final = end_final = i
    # return the max sum, and its starting and ending index
    return max_final, start_final, end_final


def maximum_sum_sub_array_circular(nums):
    """
    http://blog.sina.com.cn/s/blog_8184e03301017cip.html
    此时有环，也就是nums[-1]和nums[0]可以连接到一起，根据输入里面的正负号，可能有3种情况，最后结果为两种情况中的较大值：
    可能1：如果输入里面没有负数，则最大和为这个数组的累加和
    可能2：输入里面有负数，但此时最大和是没有跨过a[n-1]到a[0]，即和非环形数组一样
    可能3：输入里面有负数，但此时最大和是跨过a[n-1]到a[0]的，此时，负数的存在会有哪些特别呢？
        数组里面会存在一个最小和子数组，且这个最小和一定是负数，否则应当加入到最后的结果中因为有贡献
        可以这样理解：n个数的和是一定的，如果在这n个数中找到连续的一段数，是所有连续数的和最小的一段（且为负数）
        那么所有元素的和，在排除这段为负的最小和子数组之后，得到的sum一定是最大的
        此时，可以将原问题转化为，找到数组的最小子数组和min_sum，再用数组全部元素的和total_sum减去min_sum（实际上是相加因为是负数）
        那么结果一定是跨过a[n-1]到a[0]情况中最大的子数组和
    """
    max_kadane_case1 = maximum_sum_sub_array_kadane(nums)
    # 计算出累加和，并把所有元素换符号，再次用kadane求得子数组最大和，就是原数组中的子数组最小和（变了符号）
    total_run_sum = sum(nums)
    for i in xrange(0, len(nums)):
        nums[i] = -nums[i]

    min_sum_inverted = maximum_sum_sub_array_kadane(nums) # 此时符号为负数，所以下边减法变成加法
    max_wrap_kadane_case2 = total_run_sum + min_sum_inverted

    return max(max_wrap_kadane_case2, max_kadane_case1)


a = [11, 10, -20, 5, -3, -5, 8, -13, 10]
print maximum_sum_sub_array_circular(a)


def maximum_sum_sub_array_circular_copy(nums):
    """
    若元素全为非负数，则最大和为所有元素相加。
    否则，把该环形数组从某一点展开，连写两遍（复制一份接到自己后面），然后当成无环的数组求最大子数组和
    但这里要限制一个条件，就是最大子数组的长度不可以超过n，所以求的时候要注意判断，不太好容易实现
    """
    pass
