class NumArray(object):
    # https://leetcode.com/problems/range-sum-query-immutable/
    def __init__(self, nums):
        self.nums = nums
        self.rollSums = [nums[0]]
        for n in nums[1:]:
            self.rollSums.append(self.rollSums[-1] + n)

    def sumRange(self, i, j):
        return self.rollSums[j] - self.rollSums[i] + self.nums[i]

def test1():
    nums = [-2, 0, 3, -5, 2, -1]
    na = NumArray(nums)
    for i, j in [[0, 2], [2, 5], [0, 5]]:
        print na.sumRange(i, j)

