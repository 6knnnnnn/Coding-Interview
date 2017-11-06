# -*- coding: utf-8 -*-

# 很多链表节点问题都可以用stack来处理，只不过要用额外的空间，或者类似的递归方法

from utility.entity import RandomListNode


def reverse_linked_list(head):
    # https://leetcode.com/problems/reverse-linked-list/description/
    def recursion(head):
        if head is None or head.next is None:
            return head
        next = head.next
        head.next = None
        new_head = recursion(next)
        next.next = head
        return new_head

    if not head or not head.next:
        return head
    x = head
    y = head.next
    x.next = None
    while y:
        # ?<-x  y->z->?
        z = y.next
        y.next = x
        x = y
        y = z
        # ?<-x<-y  z->?
    return x


def reverse_linked_list_range(head, m, n):
    """
    https://leetcode.com/problems/reverse-linked-list-ii/description/
    """


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


def copy_list_with_random_pointer(head):
    """
    https://leetcode.com/problems/copy-list-with-random-pointer/description/

    给定一个linked list，里面的node除了有next之外还有random pointer，要求把这样的linked list完成的copy出来。

    解法1：  第一次遍历linked list，copy每个node，同时用hash map记录random pointer的关系，这里面key就是node本身
            之后再次遍历生成的linked list，在遍历的同时复制random pointer link，时间空间O(N)
    解法2：  如果可以改变input的结构，可以扫两边
            1st: (1) -> (1)’ -> (2) -> (2)’, keep random unchanged
            2nd: old.next.random (new.random) = old.random.next
            3rd: de-link (1) ->(1)’ -> (2) -> (2)’, to (1)’ -> (2)’
    """
    def hash_map():
        current = RandomListNode(0)
        new_head = current
        node_map = {}
        old = head
        # First, create new list w/o random pointer and a map of old -> new
        while old:
            current.next = RandomListNode(old.label)
            current = current.next
            node_map[old] = current
            old = old.next
        old, current = head, new_head.next
        # second, change new list's random pointer
        while old:
            current.random = node_map.get(old.random)
            current = current.next
            old = old.next
        return new_head.next

    def smart_copy():
        if not head:
            return None
        current = RandomListNode(0)
        new_head, old = current, head
        # 1st, copy label and concatenate old and new
        # 1 -> 1' -> 2 -> 2' -> 3 -> 3'...
        while old:
            current.next = RandomListNode(old.label)
            current = current.next
            current.next = old.next
            old.next = current
            old = old.next.next
        # 2nd, copy old.random.next as current.random
        # before current 1 -> 1' -> 2 -> 2' -> 3 -> 3'
        # before old     1 ~> 3 ~> 2
        # after new_head  1'~> 3'~> 2'
        old, current = head, new_head
        while old and old.next:
            if old.random:# copy
                current.random = old.random.next
            new_head = old.next
            old = old.next.next # old moves twice
        # 3rd, delink by jumping twice
        current = new_head
        while current and current.next:
            current.next = current.next.next
            current = current.next

        return new_head.next
