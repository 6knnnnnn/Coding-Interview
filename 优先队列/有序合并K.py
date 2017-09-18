# -*- coding: utf-8 -*-

from utility import ListNode


def merge_k_sorted_linked_list(list_heads):
    """
    https://leetcode.com/problems/merge-k-sorted-lists/description/
    用优先队列，初始化为每个head节点进入队列，长度<=K，max heap，因为要找最小值
    然后每次从里面找到最小的head，更新方式为，找到head的下一个node加入到队列中去（如果有的话）
    follow up可能是，merge K sorted arrays，类似的想法，heap里面需要存放对应的哪个array，以及该array的遍历index
    """
    from heapq import heappop, heapreplace, heapify
    new_head = result_node = ListNode(0)
    heap = [(n.val, n) for n in list_heads if n]
    # 初始化max heap
    heapify(heap)
    while heap:
        curr_node = heap[0][1]
        if curr_node.next:
            # heap replace: Pop and return the current smallest value, and add the new
            heapreplace(heap, (curr_node.next.val, curr_node.next))
        else:
            # 此时heap size-1，因为curr node没有后继节点了
            heappop(heap)
        # 更新结果
        result_node.next = curr_node
        result_node = result_node.next
    return new_head.next

