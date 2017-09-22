# -*- coding: utf-8 -*-


def palindrome_linked_list(head):
    """
    https://leetcode.com/problems/palindrome-linked-list/description/
    判断一个链表是否是回文的。暴力解法直接用一个stack，然后一次比较stack中的值和head开始，是否相同。
    或者把list partition分成左右两部分（用快慢指针），然后逆序其中一个，然后比较左右两部分是否一样。
    """
    fast = slow = head
    # find the mid node
    while fast and fast.next:
        fast, slow = fast.next.next, slow.next
    # reverse the second half
    reverse_head = None
    while slow:
        nxt = slow.next
        slow.next = reverse_head
        reverse_head = slow
        slow = nxt
    # compare the first and second half nodes
    while reverse_head:  # while node and head:
        if reverse_head.val != head.val:
            return False
        reverse_head = reverse_head.next
        head = head.next
    return True


def palindrome_number(x):
    """
    https://leetcode.com/problems/palindrome-number/description/
    判断一个数字是否是回文，最简单的转换成string，但是需要额外空间，或者把数字逆序之后，判断是否跟输入一样。
    """
    # x= 10 * x / 10 + x % 10
    if x < 0:
        return False
    y = 0
    cp = x
    while x > 0:
        y = y * 10 + x % 10
        x = x / 10
    return cp == y
