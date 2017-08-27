# -*- coding: utf-8 -*-


class PreSucBST(object):
    @staticmethod
    def in_order_successor_iterative(root, p):
        """
        https://leetcode.com/problems/inorder-successor-in-bst/description/
        如果root >  p，说明后继节点在左边，问题改为在root.left中找到后继
        如果root <= p，说明后继节点在右边，问题改为在root.right中找到后继
        当root变为None的时候，说明要么找到了succ，要么是不存在succ，即p比right most还要大
        """
        succ = None
        if root and p:
            while root:
                if p.val < root.val:
                    # 当去往左子树的时候，successor一定存在
                    # 此时，p在左子树中的successor可能是当前的root
                    succ = root
                    root = root.left
                else:
                    # root和p相等的时候，也需要向右边走，因此后继比p大，只可能在右边
                    # 如果是一直往右边走，有可能不存在，但只要有一次往左边走，一定存在
                    root = root.right
        return succ

    @staticmethod
    def in_order_successor_recursive(root, p):
        if not root:
            return None
        if root.val <= p.val:
            return PreSucBST.in_order_successor_recursive(root.right, p)
        else:
            left = PreSucBST.in_order_successor_recursive(root.left, p)
            return left if left else root

    @staticmethod
    def in_order_predecessor_recursive(root, p):
        if not root:
            return None
        if root.val >= p.val:
            return PreSucBST.in_order_predecessor_recursive(root.left, p)
        else:
            right = PreSucBST.in_order_predecessor_recursive(root.right, p)
            return right if right else root


class IteratorBST(object):
    """
    https://leetcode.com/problems/binary-search-tree-iterator/description/
    中序遍历迭代器：stack存放临时节点，最多O(H)个，每次next时间复杂度O(H)
    每次next，都需要把需要pop出的node的右子树的左边界，整体都放到stack中临时保存
    """
    def __init__(self, root):
        self.stack = list([])
        self.push_left(root)

    def push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def has_next(self):
        return len(self.stack) > 0

    def next(self):
        node = self.stack.pop()
        self.push_left(node.right)
        return node
