# -*- coding: utf-8 -*-


def remove_element(nums, val):
    """
    https://leetcode.com/problems/remove-element/description/
    把所有等于val的值，放到输入数组的后边，然后输出最新的数组的长度
    双指针 i 和 j，开始的时候分别指向第一个和最后一个元素，挪动i和j，找到val的时候挪动j
    """
    if nums:
        i, j = 0, len(nums) - 1
        while i <= j:
            if nums[i] == val:
                # 找到了i = val的时刻，挪动j
                while j >= i and nums[j] == val:
                    j -= 1
                if j >= i:
                    nums[i] = nums[j]
                    j -= 1
            i += 1
        return j + 1
    return 0


def remove_duplicates_from_sorted_array(nums):
    """
    https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/
    把重复的数字挪到后边去，返回新的长度
    用两个pointer，tail和i，最后返回tail对应的位置作为新的长度
    [0, tail] 里面没有重复，[tail, i] 里面有跟[0, tail]重复的数字， [i, end] 还没处理
    比如输入 1, 1, 2, 3... 得到
    1 2 3    3 ... end
    0   tail i ... end
    """
    if not nums:
        return 0
    tail = 0
    for i in xrange(1, len(nums)):
        # 从第2个开始，即i=1
        if nums[i] != nums[tail]:
            # not dup, swap tail+1 <> i
            tail += 1
            nums[tail] = nums[i]
    return tail + 1


def remove_duplicates_from_sorted_array_at_most_twice(nums):
    """
    https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/
    把重复的数字"挪到"后边去，返回新的长度，这里重复2次也不需要挪到后边
    其实这里并不需要真的把重复数字"挪到"后边去，只要找到重复次数超过2的数字，然后把后边的值挪到前边来就好了

    此时需要维持两个pointer：value pointer，以及指向最后满足条件的长度index，即nums[0...index]
    关键点：这个index pointer何时更新？

    根据条件可以断定，最后的结果，排序数组A，所有的数字A[i]，都需要满足A[i] > A[i-2]，即只关心i-2而非上一道题的i-1
    所以每次先移动遍历数组的value pointer，跟nums[i-2]比较大小来更新index，如果大于nums[i-2]，说明nums[i]

    1st: 1 2 3 3 3 4        2nd: 1 2 3 3 3 4        3rd: 1 2 3 3 3 4  此时，n == nums[i-2]，即i位置重复次数超过2
             i                         i                         i
             n                         n                         n
    4th: 1 2 3 3 3 4    这里又重新满足了 n > nums[i-2]，所以可以把 nums[i] = n，也就是把后边的值搬到了前边来
                 i
                   n
    结果：1 2 3 3 4 4
                 i
    """
    if not nums:
        return 0
    if len(nums) <= 2:
        return len(nums)
    i = 2  # i -> index pointer，从2开始
    for n in nums[2:]:  # n -> value pointer
        if n > nums[i - 2]:
            # duplicated more than 2 times
            nums[i] = n
            i += 1
    return i
