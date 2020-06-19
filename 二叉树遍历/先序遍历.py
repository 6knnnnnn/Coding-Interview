# -*- coding: utf-8 -*-
from utility.entity import TreeNode

def flatten_binary_tree_to_linked_list(root):
    """
    https://leetcode.com/problems/flatten-binary-tree-to-linked-list/description/
    把一个二叉树变成链表，要求inplace，也就是把node.right当做是node.next，举例：
         1
        / \
       2   5
      / \   \
     3   4   6
    结果变为 1->2->3->4->5->6
    其实就是先序遍历，下一次访问的时候，确保先访问left在访问right
    """
    def bfs(root):
        stack = list([root])
        while stack:
            node = stack.pop()
            if node.right:
                stack.append(node.right)
            # 先把right放进去，然后才是left，所以node.next = left
            if node.left:
                stack.append(node.left)
            if stack:
                node.right = stack[-1]
            # 需要de link
            node.left = None

    def dfs(node):
        # return ancestor and its right most node
        right_most = node
        if node:
            if node.left and node.right:
                new_left, left_right_most = dfs(node.left)
                new_right, right_most = dfs(node.right)
                node.right = new_left  # the ancestor of left subtree
                left_right_most.right = new_right
            elif node.left:  # only left child
                node.right, right_most = dfs(node.left)
            elif node.right:  # only right child
                temp, right_most = dfs(node.right)
            # else: right_most = None # leaf has no right_most node
            node.left = None  # delink root.left with original
        return node, right_most


def flatten_binary_tree_to_doubly_linked_list(root):
    """
    https://leetcode.com/problems/flatten-binary-tree-to-doubly-linked-list/description/
    """


def binary_search_tree_from_preorder(preorder):
    def recur(preorder, startIndex, endIndex):
        if startIndex >= len(preorder) or endIndex >= len(preorder) or startIndex > endIndex:
            return None

        root = TreeNode(preorder[startIndex])
        i = startIndex + 1
        while i <= endIndex:
            if preorder[i] > root.val:
                break
            i += 1
        # end of comparsion, go to left/right recursively
        root.left = recur(preorder, startIndex + 1, i - 1)
        root.right = recur(preorder, i, endIndex)
        return root

    if not preorder:
        return None
    return recur(preorder, 0, len(preorder) - 1)
