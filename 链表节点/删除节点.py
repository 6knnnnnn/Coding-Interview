# -*- coding: utf-8 -*-

from utility.entity import ListNode


def remove_duplicates_from_sorted_list(head):
    """
    https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/
    :param head:
    :return:
    """


def remove_nth_node_from_end_of_list(head, n):
    """
    https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
    删除倒数第N个节点。扫两边，先是找到总长度，然后从头开始数，倒数第N个的时候，把它删除。
    扫一遍：两个指针，快指针先是从head开始走到第n+1各节点，然后同时移动slow和fast，直到fast为None
    此时，slow就是对应的从后往前的第n-1个node，slow.next就是第Nth node，删除掉slow.next即可。
    """
    # 假头来处理特殊情况
    fake_head = ListNode(0)
    fake_head.next = head
    slow = fast = fake_head
    while n >= 0:  # to the n+1 node
        n -= 1
        fast = fast.next
    while fast:
        slow, fast = slow.next, fast.next
    # slow is the n-1 th from end
    slow.next = slow.next.next
    return fake_head.next
