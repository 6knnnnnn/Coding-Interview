# -*- coding: utf-8 -*-
from utility.entity import ListNode


def merge_sort_into_another(nums1, m, nums2, n):
    """
    https://leetcode.com/problems/merge-sorted-array/description/
    假定nums1有足够空间，把nums2的前n个元素，和nums1中前m个元素，merge到nums1中去。
    逆序处理，因为我们最后要得到的是nums[0:m+n-1]，所以需要从最后一个位置开始，即m+n-1
    每次m-1代表nums1的最后一个，n-1代表nums2的最后一个，m+n-1就是最后的nums1' 的最后一个
    """
    while m > 0 and n > 0:
        if nums1[m - 1] >= nums2[n - 1]:
            nums1[m + n - 1] = nums1[m - 1]
            m -= 1
        else:
            nums1[m + n - 1] = nums2[n - 1]
            n -= 1
    if n > 0:
        # 最后表明nums2还有元素merge到nums1中去，此时nums1中所有比nums2大的元素都已经挪到了后边
        # 所以直接把nums2剩余元素加到nums1中去
        # 如果n==0但是m>0，nums1有元素未处理，但是这些元素已经在正确的位置上去了（已排序），所以不需要考虑m>0
        nums1[:n] = nums2[:n]


def sort_linked_list(head):
    """
    https://leetcode.com/problems/sort-list/description/
    用merge sort，因为不需要用到index，用快慢指针把list partition分为两部分
    """
    def merge(h1, h2):
        dummy = tail = ListNode(None)
        while h1 and h2:
            if h1.val < h2.val:
                tail.next, tail, h1 = h1, h1, h1.next
            else:
                tail.next, tail, h2 = h2, h2, h2.next
        tail.next = h1 if h1 else h2
        return dummy.next

    if not head or not head.next:
        return head

    pre, slow, fast = None, head, head
    while fast and fast.next: # partition
        pre, slow, fast = slow, slow.next, fast.next.next
    pre.next = None
    l1 = sort_linked_list(head)
    l2 = sort_linked_list(slow)
    return merge(l1, l2)


def smaller_sum_in_array(nums):
    """
    https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/
    Count of Smaller Numbers After Self
    数组小和问题
    """
    return
