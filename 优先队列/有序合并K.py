# -*- coding: utf-8 -*-

from utility.entity import ListNode
from heapq import heappop, heapreplace, heapify
from Queue import PriorityQueue


def merge_k_sorted_linked_list(list_heads):
    """
    https://leetcode.com/problems/merge-k-sorted-lists/description/
    用优先队列，初始化为每个head节点进入队列，长度<=K，max heap，因为要找最小值
    然后每次从里面找到最小的head，更新方式为，找到head的下一个node加入到队列中去（如果有的话）
    follow up可能是，merge K sorted arrays，类似的想法，heap里面需要存放对应的哪个array，以及该array的遍历index
    """
    new_head = result_node = ListNode(0)
    heap = [(n.val, n) for n in list_heads if n] # n.val就是heap的priority
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


def merge_k_sorted_array(arrays):
    """
    https://leetcode.com/problems/merge-k-sorted-arrays/description/
    给定一个array，里面有K个sorted array，merge他们
    用一个priority queue，里面每一个node有三个信息：元素的值，目前所属于的array index，在这个array里面属于第几个元素
    """
    k = len(arrays)
    pq = PriorityQueue(k)
    for i, array in enumerate(arrays):
        pq.put((array[0], i, 0))
    result = []
    while not pq.empty():
        # value array_i element_i
        value, array_i, element_i = pq.get()
        result.append(value)
        if element_i < len(arrays[array_i]) - 1:
            # 说明此时对应的array还没遍历结束，需要继续
            new_element = (arrays[array_i][element_i + 1], array_i, element_i + 1)
            pq.put(new_element)
    return result


class KSortedArrayIterator(object):
    def __init__(self, arrays):
        """
        类似于merge_k_sorted_array，这里面实现一个iterator用来遍历元素。
        """
        self.arrays = arrays
        self.pq = PriorityQueue(len(arrays))
        for i, array in enumerate(arrays):
            self.pq.put((array[0], i, 0))

    def next(self):
        if not self.has_next():
            raise IndexError("All elements iterated. No more element.")
        value, array_i, element_i = self.pq.get()
        if element_i < len(self.arrays[array_i]) - 1:
            # 说明此时对应的array还没遍历结束，需要加入到PriorityQueue里面之后继续
            new_element = (self.arrays[array_i][element_i + 1], array_i, element_i + 1)
            self.pq.put(new_element)
        return value

    def has_next(self):
        return not self.pq.empty()


arrays = [[40,50,60],[1,2,3],[15,25],[4,5,20]]


iter = KSortedArrayIterator(arrays)

while iter.has_next():
    print iter.next()
