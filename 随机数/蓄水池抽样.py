# -*- coding: utf-8 -*-

"""
蓄水池抽样：在空间有限的情况下如何进行海量数据的随机选取，也就是找到等价的抽样方式
    有一个能递增的方式吐球的机器，每次吐一个新球N
    但空间有限无法保存所有已经吐出来的N个球的个数
    而此时假定一个只能够装K个球的袋子，袋子中装的都是前N个球等概率随机的选择的结果。
    如何实现一中球进袋子和出袋子的策略，使得仅通过这个袋子，就可以实现等价于无限空间的方法？
方法 + 证明
    当第X次吐球时，袋子中有K个球，袋子外有X-K个球，之后以K/X的概率看X中没中袋子
    1. 如果X没有被选中进入袋子，那么X就是要返回的随机结果
        1）X没有被选中进入袋子概率为(X-K)/X，但是处在球袋外的球，目前有X-K
        2）所以如果返回的是X，就代表概率=X没有进袋子 + X被选中为结果，也就是(X-K)/X * 1/(X-K) = 1/X
        3）但不保存这个球X的历史，继续下一次吐球，因为空间有限
    2. 如果X被选中进袋子，那么找到被X替换的球Y，就是要随机返回的结果
        1）X被选中进入袋子概率为K/X
        2）对于在袋子里面的K个球，每一个均有K/X * 1/K = 1/X 的概率被选中
        3）也就相当于这个被球X替换的球Y，就是新的一次的随机选的结果，被选中概率为1/X
    3. 这就等价于，对于前X个球，每一个被选中的概率为1/X

而且蓄水池取样也适用于，海量数据可能有更新的情况，而非预先处理输入的index然后随机得到其中的一个区域。
而且，蓄水池平均时间复杂度为O(1)，因为每次只需要一个新的元素即可。
"""

from 链表节点 import ListNode
import random


class LinkedListRandomNodeReservoir(object):
    """
    https://leetcode.com/problems/linked-list-random-node/description/
    其实就是蓄水池抽样的变体，此时吐球的机器就是linked list iterator
    可能要考虑linked list是可变的情况，比如新加入或者删除更新一个node，此时可以从新初始化蓄水池
    """
    def init_reservoir(self):
        # 每次初始化当前node 为 head
        self.current_node = self.original_head
        while self.reservoir:
            # 清空reservoir里面的元素，保证初始为原始的前K个元素
            self.reservoir.pop()
        while self.current_node and len(self.reservoir) < self.K:
            self.reservoir.append(self.current_node.val)
            self.current_node = self.current_node.next
        self.X = len(self.reservoir)
        if self.current_node:
            # 说明head的长度比K要大，所以从K+1开始
            self.X += 1

    def __init__(self, head):
        # 用一个array来当做reservoir，如果需要替换，直接用index来替换即可
        # 默认K=10，X记录的是iterator当前遍历的index，也就是机器吐到了哪个球
        self.reservoir = list([])
        self.K = 10
        self.X = 0
        # original head 用来记录最开始的head，当整个链表都遍历完了，就重头开始遍历
        # current node 用来记录当前遍历linked list的节点，即iterator
        self.current_node = self.original_head = head
        self.init_reservoir()

    def get_random(self):
        # 平均时间复杂度O(1)
        if not self.reservoir:
            # 说明原始input head为None
            return None
        if self.K >= self.X:
            # 此时说明，原始输入head的长度比K+1小，只能从reservoir里面的K个元素随机选
            return random.choice(self.reservoir)
        if not self.current_node:
            # 此时说明原始输入head的长度比K大，而且整个linked list遍历完毕，需要回到原始head
            # 即从第size+1开始，reservoir里面仍旧存了size个node
            self.init_reservoir()
        rnd_number = random.randint(0, self.X)
        # x就是最新的current node，默认x没有被选中
        random_result = self.current_node.val
        if rnd_number <= len(self.reservoir):
            # 此时需要从reservoir里面选择一个node作为替换
            rnd_replace_index = random.randint(0, len(self.reservoir)-1)
            random_result = self.reservoir[rnd_replace_index]
            self.reservoir[rnd_replace_index] = self.current_node.val
        # 更新当前head和目前为止的index
        self.current_node = self.current_node.next
        self.X += 1
        return random_result


class LinkedListRandomNodeSimple(object):
    # https://leetcode.com/problems/linked-list-random-node/
    # 简化版的蓄水池解法，不需要单独用蓄水池，而是提高index
    def __init__(self, head):
        self.head = head

    def get_random(self):
        # 但问题是，每次get random方法会很耗时，因为每次都要从头到尾遍历一遍，时间O(N)
        # 但蓄水池不需要，每次都可以保证O(1)，即便是需要更新蓄水池，也是O(K)时间几乎常数
        result, node, index = self.head, self.head.next, 1
        while node:
            # 假定总长度为N，每次的长度index为X，看是否为0，概率为1/X，直到最后1/N
            # result只是记录了随机数为0的时候的节点
            if random.randint(0, index) is 0:
                result = node
            node = node.next
            index += 1
        return result.val


def test(array, count=100, is_simple=True):
    head = ListNode.array_to_nodes(array)
    # possible test cases: 1->2, 1->2->3, 1->2->...->10, 1->2->3->...->100
    print head
    if is_simple:
        linked_list_random = LinkedListRandomNodeSimple(head)
    else:
        linked_list_random = LinkedListRandomNodeReservoir(head)
    wc = {}
    for i in xrange(count):
        val = linked_list_random.get_random()
        wc[val] = wc.get(val, 0) + 1
    print wc


class RandomPickIndex(object):
    # https://leetcode.com/problems/random-pick-index/description/
    # 输入是一个数组，每次pick的结果是，在数组中target对应的value的index的一个随机选择
    # 每个value可能有多个index，但是空间有限，如何实现？
    def __init__(self, nums):
        self.nums = nums

    def pick(self, target):
        """
        跟蓄水池不同的是，这里需要输出的某个target中所有index的随机值
        而且这里限定了空间，所以每次都要遍历所有元素找到target
        如果target没有出现在nums里面，返回-1；如果只出现一次，那只能是那个唯一的index
        如果出现N次，count记录的是当前target出现的次数
        每次在0到count之间随机选择，判断是否为0，所以概率就是1/count，最后的最后，概率就是1/N
        """
        result = -1
        count = 0
        for i, num in enumerate(self.nums):
            if num == target:
                if random.randint(0, count) == 0:
                    result = i
                count += 1
        return result

