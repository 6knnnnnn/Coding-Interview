# -*- coding: utf-8 -*-
from collections import deque


def binary_tree_upside_down(root):
    """
    https://leetcode.com/problems/binary-tree-upside-down/description/
    对于每一个node，如果有右节点必为叶子节点，如果有right那么必有left；但可能没有right的同时有left
    将这个二叉树翻转，left -> root -> right 结果为 right为left，left变为root，root变为right
            1           4   1           4
           / \         / \ / \         / \
          2   3       5   2  3        5  2
         / \                            / \
        4   5                          3  1
        开始              中间         结束
    """
    def dfs_bottom_up(root):
        if not root or not root.left:
            return root
        # 先递归，再反转，一直往left走得到new root
        # 此时需要de-link原始的root和对应的left right关系，不然结构会可能组成一个cycle
        new_root = dfs_bottom_up(root.left)
        old_left, old_right = root.left, root.right
        root.left = root.right = None # de-link
        old_left.left = old_right
        old_left.right = root
        return new_root

    def bfs_top_down(root):
        # 3个pointer，对应不同层的待处理的root节点，prev, curr, next
        # 另外一个pointer，对应prev root的right node
        curr_root = root
        prev_right = prev_root = None
        while curr_root:
            next_root = curr_root.left # 当前root的left，为下一个root
            curr_root.left = prev_right # 当前left变为之前的right（最开始为None）
            prev_right = curr_root.right # 当前的right作为下一层next的prev right
            curr_root.right = prev_root # 当前节点的right为之前的root
            prev_root, curr_root = curr_root, next_root # 挪到下一层的root
        # prev root其实就是最开始的left most node，此时curr root = next root = None
        return prev_root

    return dfs_bottom_up(root)


def symmetric_tree(root):
    """
    https://leetcode.com/problems/symmetric-tree/description/
        1
       / \
      2   2
     / \ / \
    3  4 4  3
    对称树结构，即从root垂直画一个分割线，判断左边和右边是否是轴对称。
    """
    def dfs(p, q):
        if not p and not q:
            return True
        if p and q:
            left = dfs(p.left, q.right)
            right = dfs(p.right, q.left)
            return p.val == q.val and left and right
        return False

    def bfs(root):
        """否则需要知道node的index，过于麻烦
        用两个queue，第一个queue保持当前层的所有节点从左往右的遍历顺序，比如第三层就是[3, 4, 4, 3]
        然后每次拿出这个queue的前后两头，如果两个node都是none，或者不是none但是value相等，就说明这两个node是对称的
        之后再次把这两个node的left right children以对称的方式，加入到第二个queue，也就是下次要处理的queue中
        如果遍历过程中，queue元素个数为奇数，或者头和尾一个是None另一个不是，或者都不是none但是value不相等的情况，返回False
        """
        if not root:
            return True
        curr_queue, next_queue = deque([root.left, root.right]), deque([])
        while curr_queue or next_queue:
            if not curr_queue:
                # 当前queue空了，交换
                curr_queue, next_queue = next_queue, curr_queue
            while curr_queue:
                # 对称必须是偶数个node
                if len(curr_queue) % 2 != 0:
                    return False
                # 首尾各自pop出要检查的在当前层的位置上对称的node
                head, tail = curr_queue.popleft(), curr_queue.pop()
                if not head and not tail:
                    # 说明两个node都是none，继续
                    continue
                elif head and tail and head.val == tail.val:
                    # 两个都不是none，而且value相等，把对应的child node加入到下一次的queue中
                    # 注意此时需要对称的append，即head的right child先加入queue的头部，然后再是left child
                    # tail的left child先加入queue的尾部，然后才是right child
                    next_queue.appendleft(head.right)
                    next_queue.appendleft(head.left)
                    next_queue.append(tail.left)
                    next_queue.append(tail.right)
                else:
                    # 一个是None另一个不是，或者都不是none但是value不相等
                    return False
        return True
    return bfs(root)
    # return not root or dfs(root.left, root.right)

