# -*- coding: utf-8 -*-


class LRUListNode(object):
    # 基本数据结构需要定义一个doubly linked list node，里面的key用来查找cache
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = self.next = None

    def __repr__(self):
        return "%s:%s <-> %s" % (self.key, self.value, self.next)


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
        self.head, self.tail = LRUListNode(1, 1), LRUListNode(-1, -1)
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
        # 返回对应key的值，如果不存在，返回-1，否则，返回之前需要把node变成最新的node
        node = self.d.get(key)
        if node:
            self.delink_node(node)
            self.update_most_recent(node)
            return node.value
        return -1

    def put(self, key, value):
        # 新增一个，需要判断是否存在，是的话对应key的node变为最新的，不存在需要加入到LRU中
        # 关键点是，如果是新加入，需要检查capacity是否满了，如果是，需要删除掉最后一个
        node = self.d.get(key)
        if node:
            node.value = value # 更新value，即同一个key的值
            self.delink_node(node)
            self.update_most_recent(node)
        else:
            # node第一次进入cache中去
            node = LRUListNode(key, value)
            self.d[key] = node
            if len(self.d) == self.cap+1:
                # remove last node from tail.prev
                last = self.tail.prev
                self.d.pop(last.key)
                self.delink_node(last)
            self.update_most_recent(node)


def test1():
    cache = LRUCache(3)
    print cache.get("user1") # print None
    cache.put("user1", "Kun")
    print cache.get("user1") # print Kun
    cache.put("user2", "Uber")
    cache.put("user3", "Glib")
    print cache.get("user2") # print Uber
    # now cache size is full
    cache.put("user4", "Backend") # it removes the key=10 since 10 is the least recently used node
    print cache.get("user1") # print None
    print cache.get("user4") # removed from
    print cache.head


class KeyNode(object):
    def __init__(self, key, value, freq=1):
        # KeyNode中保存key（键），value（值），freq（频度），prev（前驱），next（后继）
        self.key, self.value, self.freq = key, value, freq
        self.prev = self.next = None


class FreqNode(object):
    def __init__(self, freq, prev, next):
        # FreqNode中保存freq（频度）、prev（前驱）、next（后继）
        # first（指向最新的KeyNode），last（指向最老的KeyNode）
        self.freq, self.prev, self.next = freq, prev, next
        self.first = self.last = None


class LFUCache(object):
    def __init__(self, capacity):
        """
        https://leetcode.com/problems/lfu-cache/description/
        这道题目要求是O(1)的时间复杂度，如果用priority queue，最好也是O(logk)的复杂度
        出处：http://bookshadow.com/weblog/2016/11/22/leetcode-lfu-cache/

        keyDict：从key到KeyNode的映射，freqDict：从freq到FreqNode的映射，head：指向最小的FreqNode

        head --- FreqNode1 ---- FreqNode2 ---- ... ---- FreqNodeN
                      |               |                       |
                    first           first                   first
                      |               |                       |
                   KeyNodeA        KeyNodeE                KeyNodeG
                      |               |                       |
                   KeyNodeB        KeyNodeF                KeyNodeH
                      |               |                       |
                   KeyNodeC         last                   KeyNodeI
                      |                                       |
                   KeyNodeD                                 last
                      |
                    last
        """
        self.capacity = capacity
        self.keyDict = dict()
        self.freqDict = dict()
        self.head = None

    def get(self, key):
        # 若keyDict中包含key，则更新节点频度，返回对应的value，否则，返回-1
        if key in self.keyDict:
            keyNode = self.keyDict[key]
            value = keyNode.value
            self.increase(key, value)
            return value
        return -1

    def put(self, key, value):
        """
        如果capacity为0，忽略当前操作，结束
        如果keyDict中包含key，则替换其value，更新节点频度，结束
        否则，如果当前keyDict的长度 == capacity，移除head.last（频度最低且最老的KeyNode）
        新增KeyNode(key, value)，加入keyDict，并更新freqDict
        """
        if self.capacity == 0:
            return
        if key in self.keyDict:
            self.increase(key, value)
            return
        if len(self.keyDict) == self.capacity:
            self.removeKeyNode(self.head.last)
        self.insertKeyNode(key, value)

    def increase(self, key, value):
        """
        Increments the freq of an existing KeyNode<key, value> by 1.
        """
        keyNode = self.keyDict[key]
        keyNode.value = value
        freqNode = self.freqDict[keyNode.freq]
        nextFreqNode = freqNode.next
        keyNode.freq += 1
        if nextFreqNode is None or nextFreqNode.freq > keyNode.freq:
            nextFreqNode = self.insertFreqNodeAfter(keyNode.freq, freqNode)
        self.unlinkKey(keyNode, freqNode)
        self.linkKey(keyNode, nextFreqNode)

    def insertKeyNode(self, key, value):
        """
        Inserts a new KeyNode<key, value> with freq 1.
        """
        keyNode = self.keyDict[key] = KeyNode(key, value)
        freqNode = self.freqDict.get(1)
        if freqNode is None:
            freqNode = self.freqDict[1] = FreqNode(1, None, self.head)
            if self.head:
                self.head.prev = freqNode
            self.head = freqNode
        self.linkKey(keyNode, freqNode)

    def delete_freq_node(self, freq_node):
        """
        Delete freqNode.
        """
        prev, next = freq_node.prev, freq_node.next
        if prev: prev.next = next
        if next: next.prev = prev
        if self.head == freq_node: self.head = next
        del self.freqDict[freq_node.freq]

    def insertFreqNodeAfter(self, freq, node):
        """
        Insert a new FreqNode(freq) after node.
        :rtype: FreqNode
        """
        newNode = FreqNode(freq, node, node.next)
        self.freqDict[freq] = newNode
        if node.next: node.next.prev = newNode
        node.next = newNode
        return newNode

    def removeKeyNode(self, keyNode):
        """
        Remove keyNode
        :rtype: void
        """
        self.unlinkKey(keyNode, self.freqDict[keyNode.freq])
        self.keyDict.pop(keyNode.key)

    def unlinkKey(self, keyNode, freqNode):
        """
        Unlink keyNode from freqNode
        :rtype: void
        """
        next, prev = keyNode.next, keyNode.prev
        if prev: prev.next = next
        if next: next.prev = prev
        if freqNode.first == keyNode:
            freqNode.first = next
        if freqNode.last == keyNode:
            freqNode.last = prev
        if freqNode.first is None:
            self.delete_freq_node(freqNode)

    def linkKey(self, keyNode, freqNode):
        """
        Link keyNode to freqNode
        :rtype: void
        """
        firstKeyNode = freqNode.first
        keyNode.prev = None
        keyNode.next = firstKeyNode
        if firstKeyNode:
            firstKeyNode.prev = keyNode
        freqNode.first = keyNode
        if freqNode.last is None:
            freqNode.last = keyNode
