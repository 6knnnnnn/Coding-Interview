# -*- coding: utf-8 -*-


class LRUListNode(object):
    # 基本数据结构需要定义一个doubly linked list node，里面的key用来查找cache
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = self.next = None


class LRUCache(object):
    """
    https://leetcode.com/problems/lru-cache/description/
    用一个hash map，记录cached key -> LRUListNode
    还有一个双向链表，head -> n1 -> n2 -> ... nk -> tail，n1代表most recent
    需要两个helper function: delete node, update_most_recent
    """
    def __init__(self, capacity):
        self.cap = capacity
        self.d = {}
        # head 和 tail 只是placeholder，并没有实际作用，"假头"
        self.head, self.tail = LRUListNode(0, 0), LRUListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def delink_node(self, node):
        # 把node de-link掉，即从list里面"摘掉"，但在这之前需要把node的next和prev连起来
        node.prev.next = node.next
        node.next.prev = node.prev

    def update_most_recent(self, node):
        # 更新node为最新的cached node，也就是加到head后边成为most recent
        if node:
            curr_most_recent = self.head.next # 先找到当前最recent的
            node.next = curr_most_recent
            curr_most_recent.prev = node
            node.prev = self.head
            self.head.next = node

    def get(self, key):
        # 返回对应key的值，如果不存在，返回-1，否则，返回之前需要把node从
        node = self.d.get(key)
        if node:
            self.delink_node(node)
            self.update_most_recent(node)
            return node.val
        return -1

    def put(self, key, value):
        # 新增一个，需要判断是否存在，是的话对应key的node变为最新的，不存在需要加入到LRU中
        # 关键点是，如果是新加入，需要检查capacity是否满了，如果是，需要删除掉最后一个
        node = self.d.get(key)
        if node:
            node.val = value # 更新value，即同一个key的值
            self.delink_node(node)
            self.update_most_recent(node)
        else:
            node = LRUListNode(key, value)
            self.d[key] = node
            if len(self.d) == self.cap+1:
                # remove last node from tail.prev
                last = self.tail.prev
                self.d.pop(last.key)
                self.delink_node(last)
            self.update_most_recent(node)
