# -*- coding: utf-8 -*-
from collections import deque


def find_k_smallest_in_binary_search_tree(root, k):
    """
    https://leetcode.com/problems/kth-smallest-element-in-a-bst/description/
    中序遍历，从最左边的node开始（因为是最小值），每次遍历到一个新的节点后，K-1，直到K=0为止
    复杂度取决于树的高度，如果tree的高度是unbalanced，时间空间最坏情况O(N)，等同于从一个sorted list里面找第K个
    如果是一个平衡树，时间复杂度O(logN + K)，空间复杂度O(logN)
    """
    def dfs(node, in_order_list):
        if node:
            if node.left and len(in_order_list) < k:
                dfs(node.left, in_order_list)
            if len(in_order_list) < k:
                in_order_list.append(node.val)
                if node.right and len(in_order_list) < k:
                    dfs(node.right, in_order_list)

    def bfs(root, k):
        if root:
            stack = list([])
            node = root
            while stack or node:
                if node:
                    stack.append(node)
                    node = node.left
                else:
                    node = stack.pop()
                    k -= 1
                    if k == 0:
                        return node.val
                    node = node.right
        return None
    top_k_list = list([])
    dfs(root, top_k_list)
    return top_k_list[-1] if k == len(top_k_list) else None


def find_k_largest_in_binary_search_tree(root, k):
    """
    类似于reverse inorder，即右->中->左
    """


def second_min_node_in_binary_tree(root):
    """
    https://leetcode.com/problems/second-minimum-target-in-a-binary-tree/description/
    找到第二小的，不能有重复。如果只是top2，用一个hash set记录就好，然后遍历所有节点，更新set，里面最多有两个数字
    记录tree里面最小的两个，同时可以去重复
    Input:
        2           2
       / \         / \
      2   5      2    2
         / \
        5   7

    Output: 5,    -1 因为不存在2nd min
    Follow up可能是，找到第K小或者第K大的，可以用heap+hash set，各自的size最多为2，set用来记录已知的top k的个数（因为要去重复）
    如果最后里面有k个不同的值，说明存在top k distinct element，返回最大值即可，否则返回-1
    """
    top2 = set([])
    if root:
        queue = deque([root])
        while queue:
            size = len(queue)
            while size:
                size -= 1
                node = queue.popleft()
                if len(top2) < 2:
                    top2.add(node.val)
                elif node.val not in top2:
                    big = max(top2)
                    if big > node.val:
                        top2.remove(big)
                        top2.add(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
    return max(top2) if len(top2) == 2 else -1
