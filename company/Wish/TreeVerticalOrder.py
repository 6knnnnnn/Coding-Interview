# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import defaultdict


class Solution(object):
    def dfs(self, node, col_index, depth):
        if node:
            self.table[col_index].append((node.val, depth))
            self.dfs(node.left, col_index - 1, depth + 1)
            self.dfs(node.right, col_index + 1, depth + 1)

    def verticalTraversal(self, root):
        self.table = defaultdict(list)
        result = list([])
        self.dfs(root, 0, 0)
        left, right = min(self.table.keys()), max(self.table.keys())
        for column in xrange(left, right + 1):
            valueDepth = self.table[column]
            valueDepth.sort(key=lambda x: x[0])
            valueDepth.sort(key=lambda x: x[1])
            result.append([v[0] for v in valueDepth])

        return result
