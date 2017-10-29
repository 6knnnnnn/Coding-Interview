# -*- coding: utf-8 -*-


def find_duplicated_number(nums):
    """
    https://leetcode.com/problems/find-the-duplicate-number/description/
    数组长度为N+1，值域1 to N，假定只有一个重复元素，但是可能重复多次，找到这个重复的值
    解法1：hash map，时间空间O(N)
    解法2：排序后，数组的index和value应该match，第一个不match的就是重复元素，O(NlogN)
    解法3：一个for loop，里面是二分搜索，每次找到比mid小的个数，如果个数小于mid，说明重复的在右边，反之在左边，时间O(NlogN)
    :param nums:
    :return:
    """


def contains_duplicates(nums):
    """
    https://leetcode.com/problems/contains-duplicate/description/
    最简单的版本，几种做法：
    1. 两层循环双指针，一个一个比较，O(N^2)时间 O(1)空间
    2. 排序后看连续的元素是否重复，O(N * logN)时间 O(1)空间
    3. 将输入list转化为哈希set判断是否长度有所减少，O(N) 时间+空间
    """
    return len(set(nums)) == len(nums)


def contains_duplicates_within_k(nums, k):
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


def contains_duplicates_within_k_t(nums, k, t):
    """
    https://leetcode.com/problems/contains-duplicate-ii/description/
    找到两个索引i和j，判断是否满足nums[i]和nums[j]的距离<=t，以及i和j的距离<=k，即坐标差不能大于k，值差不能大于t（可能会有负数）
    解法1：两层循环 + 双指针，O(N^2)时间 O(1)空间
    解法2：hash map，key仍旧是某一个number，但是这样子每次都要判断[number-t, number, number+t]是否存在，时间复杂度O(N*T)
    解法3：维持一个大小为K的 TreeMap 窗口，每次新的元素进来，挪出去index最小的元素，加入最新的元素，同时判断新的数值是否能够找到
    number - t 或者 number + t的存在，如果有就返回True。时间复杂度O(N * logK) 空间O(K)
    解法4：bucket sort，每个slot的值域是[a, a+t]，每个slot对应的bucket只存放一个元素，即属于这个slot的数字的最近的index
    对于某个数X，首先求得其对应的slot，即第 X / t，比如t=4，X=1~4为一个slot，5~9为一个slot，10~14为一个slot
    所以对于属于同一个slot里面的任意两个元素 X and Y，他们的差值最大也只是t，即|X-Y|<=t
    关键点就是要保证，bucket中总共的元素数量<=K，即如果key的数量超过K，需要删除掉expired number，也就是当前index往前数K个数字
    如果X对应的slot里面有元素Y，而我们每次遍历元素又保证只记录最新的K个数字，此时这两个数X和Y的距离<=K，满足条件
    如果X对应的slot里面没有元素，然而相邻的上下的slot里面有满足要求的数组的数字，也满足条件。否则，把X放到bucket中。
    时间O(N)，空间O(K)因为只有最新的K个元素在bucket里面
    Edge case: t=0，即|X-Y|=0 -> X=Y，那么此时t=t+1 -> slot=1即意味着任何X/1=X，其实等价于t=1，因为需要检查上下两个slot的元素
    """
    if k < 1 or t < 0:
        return False
    bucket_map = dict([])
    slot_width = t if t else t + 1
    for i, num in enumerate(nums):
        slot = num / slot_width
        # 如果对应的slot里面有元素，说明 | X-Y | <= t AND Xi - Yi <= k
        if slot in bucket_map:
            return True
        upper, lower = slot - 1, slot + 1
        # 看相邻两个slot中，是否存在满足条件的任意一个元素，
        if upper in bucket_map and abs(num - bucket_map[upper]) <= t:
            return True
        if lower in bucket_map and abs(num - bucket_map[lower]) <= t:
            return True
        if i >= k:
            # 确保bucket中只有k个元素，即删除nums[i-k]
            last_slot = nums[i-k] / slot_width
            bucket_map.pop(last_slot)
        bucket_map[slot] = num
    return False


def intersection_2_arrays(nums1, nums2):
    """
    https://leetcode.com/problems/intersection-of-two-arrays/description/
    https://leetcode.com/problems/intersection-of-two-arrays-ii/description/
    找两个数组的交集，顺序随意
    """
    def unique(nums1, nums2):
        """
        不需要记录重复的交集，直接哈希set，时间空间O(N)，或者排序其中一个，然后遍历另一个进行二分搜索，空间O(1)时间O(N * logN)
        """
        S1, S2 = set(nums1), set(nums2)
        res = list([])
        for n in S1:
            if n in S2:
                res.append(n)
        return res

    def duplicate(m, n):
        """
        重复的交集需要记录
        解法1：为一个数组建立一个词频map，遍历另一个数组，每次把对应number的count减1，如果为0则从map中删除，时间空间O(N)
        解法2：将两个数组进行排序，之后用双指针，类似于merge sort，只是这里面不需要把长的数组合并到结果里，
            因为如果短的遍历完了，说明之后就没有交集了。时间O(N * logN + N)
        解法3：如果已经排好序了，可以通过二分查找优化找到下一个开始的index，for each element in nums1, do BS in nums2
            此时的时间复杂度为O（M * logN)，假设N > M，也就是二分遍历较长的数组，顺序遍历较短的数组
            https://discuss.leetcode.com/topic/46280/o-nlgn-solution-using-sorting-and-binary-search-with-explanation/3
        Follow up问题：If input array too big to fit in memory, external sorting, e.g. merge sort with chunks
        """
        m.sort()
        n.sort()
        i, j, resL = 0, 0, []
        while i < len(m) and j < len(n):
            if m[i] == n[j]:
                resL.append(m[i])
                i, j = i+1, j+1
            elif m[i] > n[j]:
                j += 1
            else:
                i += 1
        return resL



