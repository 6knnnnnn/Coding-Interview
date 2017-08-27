# -*- coding: utf-8 -*-

from Utility import TreeNode
import sys


class BST2GreaterTree(object):
    """
    https://leetcode.com/problems/convert-bst-to-greater-tree/description/
    比它大的所有元素累加到当前节点，其实就是中序遍历的逆序，Right - Root - Left
    parent.val += right.val; then left.val += parent.val
    """
    run_sum = 0

    def convert_recursive(self, root):
        def convert(node):
            if node:
                convert(node.right)
                # 最开始的时候run sum为0，所有走到最右边的node即最大的node
                # 此时没有比他还大的node，所以+0
                self.run_sum += node.val
                node.val = self.run_sum
                convert(node.left)
        # reset as 0
        self.run_sum = 0
        convert(root)
        return root

    @staticmethod
    def convert_iterative(root):
        if not root:
            return
        stack = list([])
        run_sum = 0 # >=当前node的所有node之和
        curr = root
        while stack or curr:
            while curr:
                # 走到最右边
                stack.append(curr)
                curr = curr.right
            curr = stack.pop()
            run_sum += curr.val
            curr.val = run_sum
            # 然后去左边
            curr = curr.left
        return root


class ValidateBST(object):
    """
    https://leetcode.com/problems/validate-binary-search-tree/description/
    递归：每次有left right range；迭代：中序遍历
    """
    @staticmethod
    def recursion(root):
        def dfs(root, left_min, right_max):
            if not root:
                return True
            if left_min < root.val < right_max:
                left = dfs(root.left, left_min, root.val)
                right = dfs(root.right, root.val, right_max)
                return left and right
            return False
        return dfs(root, -sys.maxint, sys.maxint)

    @staticmethod
    def iteration(root):
        if not root:
            return True
        stack = list([])
        curr, prev = root, None
        while curr or stack:
            while curr:
                # 去往最左边
                stack.append(curr)
                curr = curr.left
            # 拿到最左边的节点，跟之前的节点prev比较，prev就是当前节点的先续节点
            curr = stack.pop()
            if prev and prev.val >= curr.val:
                return False
            # 更新当前节点去往右子树，prev记录当前节点，也就是之后右子树的root
            curr, prev = curr.right, curr
        return True
