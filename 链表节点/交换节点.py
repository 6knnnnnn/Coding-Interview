# -*- coding: utf-8 -*-


def reverse_every_k_nodes(head, k):
    """
    https://leetcode.com/problems/reverse-nodes-in-k-group/description/
    给定一个linked list，每K个节点为一组，reverse这一组的list，之后继续
    最简单的方法，用一个stack存储k个node，然后reverse里面的node，然后继续下一组，时间O(N)空间O(K)
    或者recursion，每次找到K各节点后，reverse从开头到第K个节点，然后继续。
    """
    def reverse_k(head, k, length):
        if k <= 1 or k > length:
            # 如果k比length要大，就不需要在reverse了，返回
            return head
        new_head, cur = None, head
        for _ in xrange(k):  # reverse K times
            nxt = cur.next
            cur.next = new_head
            new_head = cur
            cur = nxt
        # 现在 head其实是k-nodes 的tail了
        head.next = reverse_k(cur, k, length - k)
        return new_head
    l, node = 0, head
    # find the total length
    while node:
        l += 1
        node = node.next
    return reverse_k(head, k, l)
