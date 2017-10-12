# -*- coding: utf-8 -*-

"""
组合，其实就是枚举，但是要根据前一次枚举的结果基础上，再次枚举，即枚举顺序一般从小到大。
需要记住之前枚举的状态，还有就是，要找到枚举的终止点。
"""

from collections import deque


def combinations(k, n):
    """
    https://leetcode.com/problems/combinations/description/
    从1...N中选择K个组成一组数，找到所有的可能
    依次对N，N-1，N-2...N-K做DFS + backtracking，时间复杂度Ckn = N!/(N-K)!
    """
    def dfs(global_results, curr_combination, start, n, k):
        """ start 就是当前从第几个数开始做组合，比如 N = 5
        curr = [1, 2, 3]    start = 4, from 4 to 5: [1,2,3,4] [1,2,3,5]
        接着下一次：
        curr = [1, 2, 4]    start = 5, from 5 to 5: [1,2,4,5]
        """
        if k == len(curr_combination):
            # 当前组合是一个结果，copy生成一个新的加入到全局中
            global_results.append(list(curr_combination))
        elif len(curr_combination) < k:
            for i in xrange(start, n+1):
                curr_combination.append(i)
                dfs(global_results, curr_combination, i + 1, n, k)
                curr_combination.pop()
    results = list([])
    if 0 < k <= n and n > 0:
        dfs(results, [], 1, n, k)
    return results


def letter_combinations_phone_number(numbers):
    """
    https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/
    给定一个电话号码，找到所有可能的字母组合，比如23，所有组合["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    其实就是组合问题，edge case是对应的number不合法，比如包含1或者其他字符
    时间复杂度O(3^N)，每一层的每个节点（数字）有3个可能
    """
    def dfs(numbers, start, result_queue, phone_map):
        if start < len(numbers):
            # numbers从start位置开始，作为当前组合的起始点
            so_far = len(result_queue)
            for i in xrange(so_far):
                # 需要pop left作为排列组合的起始点，用queue可以不需要从新生成一个temp list加到结果里
                curr = result_queue.popleft()
                for c in phone_map[numbers[start]]:
                    new = "%s%s" % (curr, c)
                    result_queue.append(new)
            # start还没有到最后一个，就继续
            dfs(numbers, start + 1, result_queue, phone_map)

    phone_map = {"2": "abc", "3": "edf", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    result_list = deque([])
    if numbers:
        for c in phone_map[numbers[0]]:
            # 初始化第一位的数字
            result_list.append(c)
        dfs(numbers, 1, result_list, phone_map)
    return result_list


def factor_combinations(n):
    """
    https://leetcode.com/problems/factor-combinations/description/
    找到一个数n的所有乘法因子组合（不包括1和自己），例子 n=30，[[2, 15], [2, 3, 5], [3, 10], [5, 6]]
    思路：DFS + backtracking。每次搜索从最小的一个因子 (2) 开始到sqrt(n)为止，查看之间的数是否可以被n整除，如果可以那么有两种选择：
        1. n 除以这个因子，并计算得出另一个因子x， 保存当前结果
        2. 进行下一层搜索。factor <= sqrt(n) 是关键, 保证了没有重复解
    时间复杂度取决于n有多少种可能的因子组合
    """
    def dfs(number, current_p, so_far_path, global_res):
        """
        从current_p开始，依次+1，判断是否能够被number整除，如果是，加入到so far path
        直到n的平方根为止即可

        30 的例子，遍历的情况
        30 2 [] []
            15 2 [2] [[2, 15]]
                5 3 [2, 3] [[2, 15], [2, 3, 5]]
            10 3 [3] [[2, 15], [2, 3, 5], [3, 10]]
            6 5 [5] [[2, 15], [2, 3, 5], [3, 10], [5, 6]]
        """
        while current_p <= number ** 0.5:
            if number % current_p == 0:
                the_other_p = number / current_p
                # 生成一个新的path result，因为此时找到了一个新的可能组合
                global_res.append(so_far_path + [current_p, the_other_p])
                # 下一层，此时number变为了number / candidate_p
                dfs(the_other_p, current_p, so_far_path + [current_p], global_res)
            current_p += 1
    res = list([])
    dfs(n, 2, [], res)
    return res
