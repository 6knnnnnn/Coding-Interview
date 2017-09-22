# -*- coding: utf-8 -*-


def maximum_size_sub_array_sum_equals_k(nums, k):
    """
    https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/description/
    找到数组中，满足相加之和等于k的连续的子数组当中，长度最大的，数组中的值正负皆可。
    暴力解法：设定一个window，宽度从1到nums的长度，找到所有可能window中的和为k的最大长度，时间O(N^2) 空间O(N)
    优化解法：
        求出数组累加和run sum，run_sum[j] 代表 nums[0...j] 的累加和
        这样子就可以很快求得从nums[i...j]之间的和，即run_sum[j] - run_sum[i]
        那么问题转化为寻找满足 run_sum[j] - run_sum[i] = k 的所有nums[i, j]中，j-i最大的情况（即size最大）
        如果存在某个 run_sum[i] = run_sum[j] - k，则需要从0开始找到这个i，即nums[0...i]的run sum
        但是每次从头找都很耗时，那么需要一个hash map，记录run sum[j]的index为j，即nums[0...j]累加和的最左index
        但要注意两点：
            1）同样的累加和，这个map存放的是最先出现的，也就是最左边的index，因为要求的是max size（min则是最后出现的）
            2）如果run_sum[j]=k，即nums[0...j]的累加和=k，找到了一个可能的结果，此时长度为j-0+1=j+1，所以map初始化为{0: -1}
                即j-i=j-(-1)=j+1为新的长度（其实也是到目前j为止最大的长度）
        |__________|  X_________X
        0          i i+1         j
        如果存在 nums[0...i]，使得 run_sum[j] - run_sum[i] = k，找到run_sum[i]的最左index
    """
    max_len = 0
    if nums:
        run_sum = nums[:]
        for i in xrange(1, len(run_sum)):
            run_sum[i] += run_sum[i - 1]
        index_map = {0: -1}
        for j in xrange(len(run_sum)):
            # 根据当前的 run_sum[j] 和 k，求出来是否存在 run_sum[j] - run_sum[i]=k，即 nums[i...j] 和为k
            run_sum_i = run_sum[j] - k
            if run_sum_i in index_map:
                # 如果run_sum[i] = diff 存在历史记录中，那么找到对应的最左边的index，更新max len
                i = index_map[run_sum_i]
                max_len = max(max_len, j - i)
            if run_sum[j] not in index_map:
                # 只把index放入到map中一次，即最左边的index
                index_map[run_sum[j]] = j
    return max_len


def contiguous_subarray_sum_to_multiple_k(nums, k):
    """
    https://leetcode.com/problems/continuous-subarray-sum/description/
    找到一个只包含非负整数的数组中，是否存在长度大于2的subarray，满足累加和是k的倍数
    """



def minimum_size_sub_array_sum(nums, k):
    """
    https://leetcode.com/problems/minimum-size-subarray-sum/description/
    一个只包含正整数的array，找到里面所有满足累加和 >= k的子数组当中，长度最小的
    比如 [2,3,1,2,4,3] and k = 7，最小的subarray是 [4, 3]
    设定一个长度可以变化的windows，比如用deque，head和tail在nums中的对应位置分别为i和j
    expand规则：当window里面的累加和<k的时候，j不断地向右移动，直到[i, j-1] < k but [i, j] >= k
    shrink规则：当window里面的累加和>=k的时候，i不断地向右移动，直到[i, j] >=k but [i+1, j] < k
    每次找到一个满足[i, j] >= k 的 window，更新min len作为最后的结果。
    时间复杂度O(N)，空间复杂度O(N)，因为需要一个queue，或者只用两个变量记录i j，空间O(1)
    """
    i = j = win_sum = 0
    min_len = len(nums) + 1
    while j < len(nums):
        # while win_sum < k, expand
        while win_sum < k:
            win_sum += nums[j]
            j += 1
            if j == len(nums):
                break
        # now win_sum >= k, shrink [i, j]
        if win_sum >= k:
            while win_sum >= k and i < j:
                win_sum -= nums[i]
                i += 1
            # exit while, win_sum < k or i == j
            min_len = min(min_len, j - i + 1)
    return 0 if min_len == len(nums) + 1 else min_len
