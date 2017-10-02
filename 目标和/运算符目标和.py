# -*- coding: utf-8 -*-

from collections import defaultdict


def target_sum(nums, target):
    """
    https://leetcode.com/problems/target-sum/description/
    给定一组数组l里面为非负数，和目标target，只用+和-运算符，判断能够得到target的组合数量，第一位可以是正负号
    http://www.cnblogs.com/grandyang/p/6395843.html
    dp[i][j]表示从0到第i-1个数字，且和为j的情况总数
    初始化dp[0][0]=1，即只有一种方式
    """
    def backtracking(nums, target, start_i, dp):
        if start_i == len(nums):
            return target == 0
        if dp[start_i].get(target, 0) > 0:
            return dp[start_i][target]
        upper = backtracking(nums, target + nums[start_i], start_i + 1, dp)
        lower = backtracking(nums, target - nums[start_i], start_i + 1, dp)
        dp[start_i][target] = upper + lower
        return dp[start_i][target]
    dp = defaultdict(dict)
    return backtracking(nums, target, 0, dp)


class ExpressionTargetSum(object):
    """
    https://leetcode.com/problems/expression-add-operators/description/
    "123", 6 -> ["1+2+3", "1*2*3"]
    "105", 5 -> ["1*0+5","10-5"] 所以可以是很多位的数字组合
    "00", 0 -> ["0+0", "0-0", "0*0"]
    """
    def __init__(self, num, target):
        self.num_str = num
        self.target = target
        self.results = list([])
        if self.num_str is not None and len(self.num_str) > 0:
            self.search("", 0, 0, 0)

    def search(self, so_far_path, start, so_far_sum, prev_mult):
        """
        so_far_path：目前为止，+-* path，比如1+2+3-4*5，so_far_num：目前为止的运算结果，1+2+3-4*5 = -14
        start：从原始的num string里哪一位开始，prev mult：前一次递归，本次乘法，需要减去的前一次递归的数字
        2个需要考虑的edge case：1）int overflow 2）不能有leading zero
        这里的技巧就是，把需要下次递归中，走乘法的路线的情况下，上一次的需要减去的数字组合，记录下来
        比如12345678，so far path=1+2+3，num=6，curr=4，那么有三条路可以走：
        1）+：那么新的path=1+2+3+4，num=10，4当做是下一次递归的prev_mult，在做下一次的递归的乘法时候：
            so far path=1+2+3+4*5，num=26=10-4+4*5=26，即上一次加法，多加了一个4，这个4现在用来做乘法
        2）-：那么新的path=1+2+3-4，num=2，-4当做是下一次递归的prev_mult，在做下一次的递归的乘法时候
            so far path=1+2+3-4*5，num=-14=2-(-4)-(-4)*5=26，即上一次减法，多"减"了一个4，这个4现在用来做乘法
        3）*：那么新的path=1+2+3*4，num=15=6-3+3*4，3就是上一次递归的prev_mult，上次是加法（1+2+3），这里减去
        """
        if start == len(self.num_str):
            # 到头了，检查目前为止的组成的num，是否为target
            if self.target == so_far_sum:
                self.results.append(so_far_path)
            return
        for i in xrange(start, len(self.num_str)):
            curr = long(self.num_str[start:i + 1])
            if start == 0:
                # 初始化开始search，这道题目假设，第一个数字只能为正
                self.search(str(curr), i + 1, curr, curr)
            else:
                self.search("%s+%s" % (so_far_path, curr), i + 1, so_far_sum + curr, curr)
                self.search("%s-%s" % (so_far_path, curr), i + 1, so_far_sum - curr, -curr)
                curr_mult = prev_mult * curr
                self.search("%s*%s" % (so_far_path, curr), i + 1, so_far_sum - prev_mult + curr_mult, curr_mult)
            if curr == 0:
                # 不能有leading zero，即如果当前为0，不考虑i后边的组合了，比如105，05有leading zero就不可以
                return
