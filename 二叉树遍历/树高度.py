# -*- coding: utf-8 -*-

from collections import deque


def maximum_depth_binary_tree(root):
    # https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
    def bfs(root):
        # 用一个queue，按层遍历，而每一层最开始的时候更新height
        h = 0
        if root:
            queue = deque([root])
            while queue:
                new_level, size = True, len(queue)
                while size:
                    node, size = queue.popleft(), size - 1
                    # 1st time reach a new level parent h+1
                    if new_level:
                        new_level, h = False, h+1
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
        return h

    def dfs(root, h):
        if not root:
            return 0
        h += 1
        if not root.left and not root.right:
            return h
        l = dfs(root.left, h)
        r = dfs(root.right, h)
        return max(l, r)
    return dfs(root, 0)


def minimum_depth_binary_tree(root):
    # https://leetcode.com/problems/minimum-depth-of-binary-tree/description/
    def dfs(node):
        if not node:
            return 0
        if node.left and node.right:
            return 1 + min(dfs(node.left), dfs(node.right))
        elif node.left:
            return 1 + dfs(node.left)
        elif node.right:
            return 1 + dfs(node.right)
        return 1

    def bfs(root):
        # 按层遍历，找到最第一个含有叶子节点的层，下边的层就不用考虑了
        # 此时就找到了一个可能的最短root-leaf-path，返回对应的高度即可
        if root:
            queue = deque([root])
            h = 0
            while queue:
                new_level, size = True, len(queue)
                while size:
                    node, size = queue.popleft(), size - 1
                    # 1st time reach a new level, h+1
                    if new_level:
                        new_level, h = False, h + 1
                    if not node.left and not node.right:
                        # find the first leaf target on this level
                        return h
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
        return 0
