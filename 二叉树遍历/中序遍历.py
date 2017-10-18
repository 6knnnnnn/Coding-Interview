# -*- coding: utf-8 -*-

import sys
from utility.entity import TreeNode


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


def most_frequent_element_in_binary_search_tree(root):
    """
    https://leetcode.com/problems/most-frequent-element-in-binary-search-tree/description/
    也是中序遍历，保存两个变量，当前element frequency，全部element最大frequency
    之所以中序遍历所以因为，如果有新的元素，就可以换掉当前元素了，因为是sorted
    """


class RecoverBST(object):
    def recover_binary_search_tree(self, root):
        """
        https://leetcode.com/problems/recover-binary-search-tree/description/
        BST中两个节点n1和n2的值被交换了，导致BST不再是valid，找到这两个node，并且swap value以来恢复原始的BST
        中序遍历，理论上必须是从大到小顺序的，如果出现之前遍历的节点的值大于当前的节点，说明找到一种可能
        即n1和n2在中序遍历的顺序中是相邻的节点，而且刚好是被交换的节点
        如果之后再次遇到了这种情况，说明找到了第二个节点n2，以及n1和n2并不是相邻的中序节点，需要更新n2
        """
        def inorder(current):
            if not current: return
            inorder(current.left)
            if self.prev.val >= current.val:
                # 找到了一个invalid的情况
                if not self.n1:
                    # 如果n1为空，说明prev为第一个node
                    self.n1 = self.prev
                # n2永远指向current
                self.n2 = current
            self.prev = current
            inorder(current.right) # go to right

        self.n1 = self.n2 = None
        self.prev = TreeNode(-sys.maxint)
        inorder(root)
        self.n1.val, self.n2.val = self.n2.val, self.n1.val

    @staticmethod
    def recover_bfs(root):
        # in order left < root < right, compare current with prev
        if not root: return
        stack = list([])
        curr = root
        prev = n1 = n2 = None
        while curr or stack:
            while curr: # left most
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            if prev and prev.val>=curr.val:
                if not n1: n1=prev
                n2 = curr # n1 ... n2
            prev, curr = curr, curr.right
        n1.val, n2.val = n2.val, n1.val

