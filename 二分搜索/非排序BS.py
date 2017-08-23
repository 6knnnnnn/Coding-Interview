# -*- coding: utf-8 -*-
# 二分搜索，并不是说一定要排好序，而只要是能确定不在左边或者不在右边就能缩小搜索范围


def find_peak_element(nums):
    """
    https://leetcode.com/problems/find-peak-element/description/
    比相邻元素大的，就叫peak元素。假定输入里面相邻的元素不相等，即必定存在peak element
    而且nums[-1] = nums[n] = -∞，也就是只要nums[0]>nums[1]或者nums[n-1] > nums[n-2]，他俩也可以算是peak
    Peak element的定义，用图表示就是3种情况：
    1）一段上升直线达到peak后开始下降 2）一直上升，直到最后结束（最后一个是peak）3）一直下降，peak为第一个
    暴力解法，遍历所有，比较相邻的，找到peak
    目的是找到任意一个peak element即可，那么可以很"暴力"的二分搜索：
    1. If num[i-1] < num[i] > num[i+1], then num[i] is peak 刚好中间
    2. If num[i-1] < num[i] < num[i+1], then num[i+1...n-1] must contain a peak 右边
    3. If num[i-1] > num[i] > num[i+1], then num[0...i-1] must contain a peak 左边
    4. If num[i-1] > num[i] < num[i+1], then both sides have peak 其它
    """
    left, right = 0, len(nums) - 1
    while left < right - 1:
        mid = (left + right) >> 1
        # case 1
        if nums[mid] > nums[mid + 1] and nums[mid] > nums[mid - 1]:
            return mid
        # case 2, 去右边
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        # case 3, 去左边
        else:
            right = mid - 1
    # 只剩下两个元素
    return max(nums[left], nums[right])


def first_bad_version(v):
    """
    https://leetcode.com/problems/first-bad-version/description/
    这里的版本号输入v，是一个int，所以可以用二分搜索
    如果中间的版本是错误的，说明第一个错误版本发生在左边，否则，发生在右边
    """
    def is_bad_version(v):
        return True
    left, right = 1, v
    while left <= right:
        mid = (left + right) >> 1
        if is_bad_version(mid):
            right = mid - 1 # 去左边
        else:
            left = mid + 1 # 去右边
    # 只剩下两个元素
    return left if is_bad_version(left) else right
