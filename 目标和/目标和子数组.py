# -*- coding: utf-8 -*-
from collections import defaultdict


def maximum_size_subarray_sum_equals_k(nums, k):
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


def subarray_sum_equals_k(nums, k):
    """
    https://leetcode.com/problems/subarray-sum-equals-k/description/
    给定一个整数数组，和k，判断在数组当中有多少个subarray的和为k的情况
    解法1：建立累加和数组，然后遍历数组，每次再次遍历累加和，找到[i, j]满足累加和为k的情况的个数，时间O(N^2)
    解法2：建立起run sum freq map，即对于到目前i位置的nums来说，i之前的run sum的出现次数
    所以每当我们根据run_sum-k，找到对应diff之后，如果这个diff在freq map里面，把它的出现频率加入到结果中即可
    也就是说，我们还是用run sum，但是需要记录之前出现的次数，以避免重复搜索的情况（如果找到所有可能，就是另一回事了）
    """
    def run_sum_method(nums, k):
        run_sum = nums[:]
        for i in xrange(1, len(nums)):
            run_sum[i] += run_sum[i-1]
        res = 0
        for i in xrange(len(nums)):
            if run_sum[i] == k:
                res += 1
            for j in xrange(i):
                if run_sum[i] - run_sum[j] == k:
                    res += 1
        return res

    def frequency_map(nums, k):
        count = run_sum = 0
        run_sum_freq = defaultdict(int)
        for num in nums:
            run_sum_freq[run_sum] += 1
            run_sum += num
            count += run_sum_freq[run_sum - k]
        return count


def contiguous_subarray_sum_to_multiple_k(nums, k):
    """
    https://leetcode.com/problems/continuous-subarray-sum/description/
    找到一个只包含非负整数的数组中，是否存在长度大于2的连续的subarray，满足累加和是k的倍数
    解法1：暴力解法，根据累加和，判断是否是k的倍数；如果k是0，直接找是否有两个连续的元素均为0，时间O(N^2)
    解法2：余数定理，若数字a和b分别除以数字c，若得到的余数相同，那么(b-a)必定能够整除c
    这里面a和b分别对应着从第一个元素开始的两端累加和，即a=nums[0:i] b=nums[0:j], j > i
    那么我们用一个集合set来保存所有出现过的余数，如果当前的累加和除以k得到的余数m在set中已经存在了
    那么说明当前的累加和b，和之前的一段累加和a，相减之后，必定能整除k
    题目要求子数组至少需要两个数字，那么对于set我们需要变为hash map，用来记录之前的index，而且此时记录的是最开始的index，即最远的
    """
    def brute_force():
        for i in xrange(len(nums)):
            run_sum = nums[i]
            for j in xrange(i+1, len(nums)):
                run_sum += nums[j]
                if run_sum % k == 0:
                    return True
        return False

    if k == 0:
        for i in xrange(1, len(nums)):
            if nums[i] == 0 and nums[i - 1] == 0:
                return True
    else:
        run_sum = 0
        # 初始化map为{0: -1}，原因是需要计算index difference，即上边题目maximum_size_subarray_sum_equals_k
        m_map = {0: -1}
        for i in xrange(len(nums)):
            run_sum += nums[i]
            m = run_sum % k
            if m not in m_map:
                m_map[m] = i
            elif m_map[m] + 1 < i:
                return True
    return False


def minimum_size_subarray_sum(nums, k):
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
