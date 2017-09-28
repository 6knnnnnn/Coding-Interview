# -*- coding: utf-8 -*-

"""
在一个无序数组中，找到最小的（或者最大的）第K个数

1. Sort inplace -> find the kth, O(NlgN) time + O(1) space
2. Min heap to store the K-th largest in input, O(N + NlgK) time + O(K) space
3. Quick Selection: similar to quick sort, when the pivot element is put on X=K -> the Kth element
    O(N) best O(N^2) worst time + O(1) memory
4. Randomize the input and use quick select, O(N) time
5. BFPRT算法:
    分组，每五个数一组，每组数内部排序，但组与组之间不排序，这一步骤花费O(N)时间。
    之后，把每个组的中位数拿出来，组成一个新的数组B，再次求这个数组B的中位数，作为最后quick select的pivot
    因为中位数的特点，可以用来保证下次递归的起始和终止位置为balance，也就是最少有3/10小于pivot，最多有7/10大于pivot
    之所以是5各一组，因为收敛，时间复杂度最优。
"""
import heapq


def find_kth_largest_min_heap(nums, k):
    # https://leetcode.com/problems/kth-largest-element-in-an-array
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
    for _ in xrange(len(nums)-k):
        heapq.heappop(heap)
    return heapq.heappop(heap)


class QuickSelect(object):
    # O(n) time, quick selection
    def find_kth_largest(self, nums, k):
        # convert the kth largest to smallest
        return self.find_kth_smallest(nums, len(nums) + 1 - k)

    def find_kth_smallest(self, nums, k):
        # choose the right-most element as pivot 返回的是index
        def partition(nums, l, r):
            low = l
            while l < r:
                if nums[l] < nums[r]:
                    # swap
                    nums[l], nums[low] = nums[low], nums[l]
                    low += 1
                l += 1
            nums[low], nums[r] = nums[r], nums[low]
            return low

        if nums:
            pos = partition(nums, 0, len(nums) - 1)
            if k > pos + 1:
                return self.find_kth_smallest(nums[pos + 1:], k - pos - 1)
            elif k < pos + 1:
                return self.find_kth_smallest(nums[:pos], k)
            else:
                return nums[pos]

