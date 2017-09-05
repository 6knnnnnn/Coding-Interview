# -*- coding: utf-8 -*-
from Utility import ListNode


def merge_sort_into_another(nums1, m, nums2, n):
    # https://leetcode.com/problems/merge-sorted-array/description/
    # 假定nums1有足够空间，即把nums2所有元素挪到nums1中
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0 and i >= 0:
        if nums2[j] >= nums1[i]:
            nums1[k] = nums2[j]
            j -= 1
        else:
            nums1[k] = nums1[i]
            i -= 1
        k -= 1
    while j >= 0:
        nums1[k] = nums2[j]
        k -= 1
        j -= 1


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
