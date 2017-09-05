# -*- coding: utf-8 -*-


def find_duplicated_number(nums):
    """
    https://leetcode.com/problems/find-the-duplicate-number/description/
    数组长度为N+1，值域1 to N，假定只有一个重复元素，但是可能重复多次，找到这个重复的值
    解法1：hash map，时间空间O(N)
    解法2：排序后，数组的index和value应该match，第一个不match的就是重复元素
    解法3：一个for loop，里面是二分搜索，每次找到比mid小的个数，如果个数小于mid，说明重复的在右边，反之在左边
    :param nums:
    :return:
    """


def contain_duplicates(nums):
    """
    https://leetcode.com/problems/contains-duplicate/description/
    最简单的版本，几种做法：
    1. 两层循环双指针，一个一个比较，O(N^2)时间 O(1)空间
    2. 排序后看连续的元素是否重复，O(N * logN)时间 O(1)空间
    3. 将输入list转化为哈希set判断是否长度有所减少，O(N) 时间+空间
    """
    return len(set(nums)) == len(nums)


def contain_duplicates_within_k(nums, k):
    """
    https://leetcode.com/problems/contains-duplicate-ii/description/
    找到两个索引i和j，判断是否满足nums[i]=nums[j]以及i和j的距离<=k
    解法1：两层循环 + 双指针，O(N^2)时间 O(1)空间
    解法2：hash map，数组中的number为key，对应的index为value，每次插入一个新的index，判断是否满足，时间空间O(N)
    优化：其实只要记录最后一个index就可以了，因为之前的index如果不满足条件，那么之后的index肯定也不满足，空间仍为O(N)但是常数变小
    """
    index_map = dict([])
    for i, n in enumerate(nums):
        if n in index_map and abs(i - index_map[n]) <= k:
            return True
        # 如果n还没重复过，或者不满足i-j <= k，更新n的最大的index
        index_map[n] = i
    return False


def contain_duplicates_within_k_t(nums, k, t):
    """
    https://leetcode.com/problems/contains-duplicate-ii/description/
    找到两个索引i和j，判断是否满足nums[i]和nums[j]的距离<=t，以及i和j的距离<=k，即坐标差不能大于k，值差不能大于t
    可能会有负数
    解法1：两层循环 + 双指针，O(N^2)时间 O(1)空间
    解法2：hash map，key仍旧是某一个number，但是这样子每次都要判断[number-t, number, number+t]是否存在，时间复杂度O(N*T)
    解法3：维持一个大小为K的 TreeMap 窗口，每次新的元素进来，挪出去index最小的元素，加入最新的元素，同时判断新的数值是否能够找到
    number - t 或者 number + t的存在，如果有就返回True。时间复杂度O(N * logK) 空间O(K)
    解法4：bucket sort，每个slot的值域是[0, t+1]，对于一个数将其分到第num/(t+1)桶中，比如t=4，0~4为桶0，5~9为桶1，10~14为桶2
    对于某个数，只需要查找相同的和相邻的上下桶的元素，就可以判断有无满足条件的num[i]和num[j]，时间空间O(N)
    """
    if k < 1 or t < 0:
        return False
    bucket_map = dict([])
    for i, num in enumerate(nums):
        slot = num / (t+1)
        # 首先确定slot存在于bucket中，如果不存在则需要把当前num加入到slot对应的bucket中
        if slot in bucket_map:
            upper, lower = slot - 1, slot + 1
            # 看相邻两个slot中
            if upper in bucket_map and abs(num - bucket_map[upper]) <= t:
                return True
            if lower in bucket_map and abs(num - bucket_map[lower]) <= t:
                return True
        if len(bucket_map) >= k:
            last_slot = nums[i-k] / (t+1)
            bucket_map.pop(last_slot)
        bucket_map[slot] = num
    return False
