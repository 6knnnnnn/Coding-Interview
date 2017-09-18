# -*- coding: utf-8 -*-


def closest_binary_search_tree_value(root, t):
    # https://leetcode.com/problems/closest-binary-search-tree-value/description/
    closest = root.val
    while root:
        if abs(root.val - t) < abs(closest - t):
            # If root.val more close than closest
            closest = root.val
        # Go to the corresponding child root
        # Why this? if a < b < c
        # if t < b, then b-t < c-t 更接近的在左边
        # if t > b  then t - b > t - c 更接近的在右边
        root = root.left if root.val > t else root.right
    return closest
