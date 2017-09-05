# -*- coding: utf-8 -*-


def intersections_of_two_linked_list(head1, head2):
    """
    https://leetcode.com/problems/intersection-of-two-linked-lists/description/
    A:      a1 → a2
                   ↘
                     c1 → c2 → c3
                   ↗
    B: b1 → b2 → b3
    如果两个链表相交，返回两个链表的最初相交点
    首先找到两个链表的长度，较长的longer长度减去较短的shorter，得到的差值offset，用来处理longer链表
    即首先遍历longer，找到第offset个node作为初始点，之后同时遍历longer shorter，直到找到相等的node
    """
    def get_length(head):
        length = 0
        while head:
            length, head = length + 1, head.next
        return length
    l1, l2 = get_length(head1), get_length(head2)
    longer = head1 if l1 > l2 else head2
    shorter = head2 if l1 > l2 else head1
    offset = abs(l2-l1)
    while offset:
        longer, offset = longer.next, offset - 1
    while longer and shorter:
        if longer == shorter:
            return longer
        longer, shorter = longer.next, shorter.next
    return None
