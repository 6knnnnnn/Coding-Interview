# -*- coding: utf-8 -*-


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


def symmetric_tree(tree1, tree2):
    pass
