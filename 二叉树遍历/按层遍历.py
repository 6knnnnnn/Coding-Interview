# -*- coding: utf-8 -*-

from collections import deque, defaultdict
import sys


def level_order_traversal(root):
    """
    https://leetcode.com/problems/binary-tree-level-order-traversal/description/
    按层遍历，每一层一个queue存储，该层结束后，加入到全局结果
        3
       / \
      9  20
        /  \
       15   7
    结果：[[3], [9, 20], [15, 7]]
    """
    if not root:
        return []
    queue = deque([root])
    res = list([])
    while queue:
        curr_level = list([])
        size = len(queue)
        while size:
            size -= 1
            node = queue.popleft()
            curr_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(curr_level)
    return res


def zigzag_level_order_traversal(root):
    """
    https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/
    Z字翻转，一个意思，此时需要记录每层的遍历方向，以及将left right child加到queue中的顺序
    """
    if not root:
        return []
    queue = deque([root])
    res = list([])
    left2right = True
    while queue:
        curr_level = list([])
        size = len(queue)
        while size:
            size -= 1
            if left2right: # 左 -> 右
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            else: # 右 -> 左
                node = queue.pop()
                if node.right:
                    queue.appendleft(node.right)
                if node.left:
                    queue.appendleft(node.left)
            curr_level.append(node.val)
        left2right = not left2right # 改变方向
        res.append(curr_level)
    return res


def binary_tree_vertical_order_traversal_bfs(root, sort=False):
    """
    https://leetcode.com/problems/binary-tree-vertical-order-traversal/description/
          3
        /  \
       9    8
      / \  / \
     4  0 1   7
    遍历结果：[ [4], [9], [3,0,1], [8], [7]]，要按照column number的顺序来打印结果
    根据root的左右子树，找到一个相对的column number，用一个hash table记录所有column number一样的节点
    如果题目不要求顺序输出，比如上边的[3,0,1]，如果是[1, 0, 3]输出没问题的话也可以用DFS
    但如果要求顺序，DFS比较难以实现，BFS可以用stack，每个元素包括node.val column index
    以及用一个hash table记录 column index -> list of target value
    空间O(N)，如果最后对table key进行排序的话，时间O(N + C*logC)
    C即column的总数，C<=N/2，最坏情况即是一个满树，最后一行都是叶子节点，最坏情况O(N*logN)
    如果不排序，而是用两个变量记录最大最小column的范围，额外的O(N)次比较，整体还是O(N)
    """
    col_index_table = defaultdict(list)
    res_l = []
    if not root:
        return res_l
    # FIFO, i.e. 左边比右边先进队列
    min_col, max_col = -sys.maxint, sys.maxint
    queue = deque([(root, 0)])
    while queue:
        size = len(queue)
        while size > 0:
            node, col_index = queue.popleft()
            # 更新column index的值域
            min_col = min(min_col, col_index)
            max_col = max(max_col, col_index)
            col_index_table[col_index].append(node.val)
            size -= 1
            if node.left:
                queue.append((node.left, col_index - 1))
            if node.right:
                queue.append((node.right, col_index + 1))
    if sort:
        # 需要排序的话，最坏情况多花费O(N*logN)，如果已经知道column比较小，则可以用排序
        col_index_list = col_index_table.keys()
        list.sort(col_index_list)
        for i in col_index_list:
            res_l.append(col_index_table[i])
    else:
        # 不排序，用之前找好的column值域区间，但是会有额外的O(N)次比较
        for i in xrange(min_col, max_col+1):
            res_l.append(col_index_table[i])
    return res_l


def binary_tree_vertical_order_traversal_dfs(root):
    # 如果每一个column对应的遍历顺序不重要的话，此方法也可以
    def dfs(node, col_index_table, col_index):
        if not node:
            return
        if col_index not in col_index_table:
            col_index_table[col_index] = list([])
        col_index_table[col_index].append(node.val)
        dfs(node.left, col_index_table, col_index - 1)
        dfs(node.right, col_index_table, col_index + 1)

    col_index_table = {}
    result_list = []
    dfs(root, col_index_table, 0)
    # 按照column number顺序，也就是table key
    index_list = col_index_table.keys()
    list.sort(index_list)
    for index in index_list:
        result_list.append(col_index_table[index])
    return result_list


def find_largest_value_in_each_tree_row(root):
    """
    https://leetcode.com/problems/find-largest-value-in-each-tree-row/description/
    按层遍历，找到每一层的最大值。follow up可能是 按照高度遍历，找到每个高度对应的max value
    用一个hash table记录level->max，每次遍历到一个新的level，更新该level的max，空间O(H)，时间O(N)
    或者用一个list/stack保存当前 row level max。也可以用DFS做。
    """
    row_max = list([])
    if root:
        queue = deque([root])
        # row max 记录最新level max
        while queue:
            size = len(queue)
            row_max.append(queue[0].val)
            while size:
                size -= 1
                node = queue.popleft()
                row_max[-1] = max(row_max[-1], node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
    return row_max


def binary_tree_right_side_view(root):
    """
    https://leetcode.com/problems/binary-tree-right-side-view/description/
       1            <---
     /   \
    2     3         <---
     \     \
      5     4       <---
    结果：[1, 3, 4]，也就是从右边看整棵树的结构。按层遍历，从左到右，每层最后一个就是所需要的节点。
    """
    res_list = list([])
    if root:
        q = deque([root])
        while q:
            size = len(q)
            while size > 0:
                size -= 1
                node = q.popleft()
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
                if size == 0: res_list.append(node.val)
    return res_list


class SumLeftLeaves(object):
    def __init__(self):
        self.total = 0

    def sum_of_left_leaves(self, root):
        """
        https://leetcode.com/problems/sum-of-left-leaves/description/
        这道题目有点类似于 Binary Tree Right Side View，本题要求每一层的第一个左边的节点，而且是叶子节点。
            3
           / \
          9  20
         /  /  \
        10 15   7，结果为10 + 15 = 25
        """
        def dfs(root, is_left):
            if not root:
                return
            if root.left or root.right:
                dfs(root.left, True)
                dfs(root.right, False)
            elif is_left:
                self.total += root.val

        def bfs(root):
            # 跟DFS一个意思，加入新的node到stack中去
            total = 0
            if root:
                stack = list([(root, 0)])
                while stack:
                    n, is_left = stack.pop()
                    if not n.left and not n.right:
                        if is_left:
                            total += n.val
                    if n.left: stack.append((n.left, 1))
                    if n.right: stack.append((n.right, 0))
            return total

        self.total = 0
        # root 本身不算是left child leaf
        dfs(root, False)
        return self.total


def average_levels_binary_tree(root):
    """
    https://leetcode.com/problems/average-of-levels-in-binary-tree/description/
    按层遍历，求每层的总和以及node数量
    """
    res = list([])
    if root:
        q = deque([root])  # FIFO
        while q:
            # a new level, init sum and count
            size = len(q)
            s = c = 0
            while size:  # iterate this level only
                node = q.popleft()
                size -= 1
                s, c = s+node.val, c+1
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(float(s) / float(c))  # new avg
    return res
