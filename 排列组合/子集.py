# -*- coding: utf-8 -*-

# N个唯一的数，包含空集的子集数2^N，不包含全集的真子集 2^N-1


def subset_unique(nums):
    # https://leetcode.com/problems/subsets-ii/description/
    def subsets_unique_recur(nums):
        # 回溯法+DFS，每次把path加到结果中，然后递归
        # 新的path就是当前path加上新的一个元素i，为了避免重复，下次递归从i+1开始
        def dfs(start, path):
            res.append(path)  # path = subset
            for i in xrange(start, len(nums)):
                dfs(i + 1, path + [nums[i]])
        res = []
        dfs(0, [])
        return res

    def subsets_unique_iter(nums):
        # 空集也算子集，而且空集和单一元素可以组成单个元素的子集，所以要从空集开始
        res = [[]]
        for n in nums:
            # 每次都是从前一次得到的结果，枚举所有可能，求下一轮的子集
            for i in xrange(len(res)):
                new_subset = [res[i] + [n]]
                res += new_subset
        return res


def test1():
    """
    [[]] 初始化
    [[], [1]]  只有1
    [[], [1], [2], [1, 2]] 只有1，2
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]] 只有1，2，3
    但是如果是有重复的，就不行了：nums = [1, 2, 2, 3]
    [[], [1]]
    [[], [1], [2], [1, 2]]
    [[], [1], [2], [1, 2], [2], [1, 2], [2, 2], [1, 2, 2]]
    """


def subsets_duplicated(nums):
    """
    https://leetcode.com/problems/subsets-ii/description/
    如何去重复？需要先进行排序，如果对于元素i，他和i-1相等，即重复，只需要在将它和一部分已经存在的subset进行组合
    关键点：如何找到目标subset？也就是，在当前存在的subset list中，从哪个index j开始，把当前重复的i跟他们进行组合操作？
    答案：之前根据i-1所创建的subset就不用考虑了

    假设排序input后：[1, 2, …. X, d1, d2, ….] 1-X均为唯一, d1=d2 且均不等于 1...X
    当 i = X  的时候，结果中创建了 2^X个元素（即从第一个开始到第X个）
    当 i = d1 的时候，结果中创建了 2^(X+1)个元素，即 [1...2^X, 2^X+1...2^X]
    当 i = d2 的时候，对于结果中的 [1...2^X] 这段，就不需要考虑了
        因为这段已经和d1创建出了属于他们的subset，没有必要在和d2再次组合成subset了，但是[2^X+1...2^X]这段是需要和d2组合的

    例子：nums = [1, 2, 2, 3]，刚开始 n = 1，得到[[], [1]]
    到第1个2的时候：[[], [1], [2], [1, 2]]，此时满足 i != i-1，得到j=2，之后再创建出新的subsets
    到第2个2的时候，我们不需要考虑[], [1]，只需要考虑[2], [1, 2]，所以就有：[[], [1], [2], [1, 2], [2, 2], [1, 2, 2]]
    """
    res = [[]]
    nums.sort()
    j = 0
    for i, n in enumerate(nums):
        if i == 0 or n != nums[i - 1]:
            # 此时代表没有重复的情况，即要么i=0，要么当前n和i-1不等，j就是len(res)，下边的k也就是从0开始的了
            j = len(res)
        # 如果有重复，即i=i-1，j记录的是对应的上一次i-1所创建的subset的长度，那么这些就不需要考虑了，直接从len(res)-j开始k
        for k in xrange(len(res) - j, len(res)):
            res.append(res[k] + [n])
    return res
