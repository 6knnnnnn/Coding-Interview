# -*- coding: utf-8 -*-

# N个唯一的数，包含空集的子集数2^N，不包含全集的真子集 2^N-1


def subsets_unique_recur(nums):
    # 回溯法+DFS，每次把path加到结果中，然后递归
    # 新的path就是当前path加上新的一个元素i，为了避免重复，下次递归从i+1开始
    def dfs(start, path):
        print res
        res.append(path)  # path = subset
        for i in xrange(start, len(nums)):
            dfs(i + 1, path + [nums[i]])
    res = []
    dfs(0, [])
    return res


def subsets_unique_iter(nums):
    # 空集也算子集，而且空集+单一元素可以组成单个元素的子集
    res = [[]]
    for n in nums:
        # 每次都是从前一次得到的结果，枚举所有可能，求下一轮的子集
        for i in xrange(len(res)):
            new_subset = [res[i] + [n]]
            res += new_subset
        print res
    return res


def test1():
    nums = [1,2,2,3]
    subsets_unique_iter(nums=nums)
    print "----"
    subsets_unique_recur(nums=nums)

"""
没有重复
    [[], [1]]
    [[], [1], [2], [1, 2]]
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
如果有重复？
    nums = [1,2,2]
    subsets_unique_iter(nums=nums)
    [[], [1]]
    [[], [1], [2], [1, 2]]
    [[], [1], [2], [1, 2], [2], [1, 2], [2, 2], [1, 2, 2]]
"""

