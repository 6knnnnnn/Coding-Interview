# -*- coding: utf-8 -*-

from collections import deque, defaultdict
import sys
from utility.entity import TreeNode


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
    根据root的左右子树，找到一个相对的column numbers，用一个hash table记录所有column number一样的节点
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
    min_col, max_col = sys.maxint, -sys.maxint
    queue = deque([(root, 0)])
    while queue:
        size = len(queue)
        while size > 0:
            node, col_index = queue.popleft()
            # 更新column index的值域
            min_col = min(min_col, col_index)
            max_col = max(max_col, col_index)
            col_index_table[col_index].add(node.val)
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
        col_index_table[col_index].add(node.val)
        dfs(node.left, col_index_table, col_index - 1)
        dfs(node.right, col_index_table, col_index + 1)

    col_index_table = defaultdict(list)
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
            # 每次有新的一层，记录当前层的临时max，之后当前层每次都要更新
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
                    if not n.left and not n.right and is_left:
                        total += n.val
                    if n.left:
                        stack.append((n.left, 1))
                    if n.right:
                        stack.append((n.right, 0))
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


class TreeLinkNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.next = None


def populating_next_right_pointers_in_each_node(root):
    """
    https://leetcode.com/problems/populating-next-right-pointers-in-each-node/description/
    假设一个二叉树，里面的节点除了left和right之外，还有一个next节点，该节点初始的时候为None
    现在要把整个二叉树的每一个节点的next指向该节点在该层的下一个right节点，也就是从左向右遍历的顺序
         1                           1 -> NULL
       /  \                        /  \
      2    3                      2 -> 3 -> NULL
     /    / \                    /    / \
    4    6  7                   4 -> 6->7 -> NULL

    如果是一个满二叉树，DFS和BFS都能很简单的解决。如果可以是任意的二叉树，BFS能解两种情况，但DFS这种情况edge case很复杂。
    但如果要求是O(1)空间的话，需要有一些trick：
        这里面，每一层相当于一个linked list，而且遍历当前层的时候，也是在为下一层做准备，相当于同时遍历两层。
        即每次遍历第x层的时候，除了把本层的next连接起来之外，也要把x+1层的node用next连起来
        满二叉树的情况要简单一些，因为有left则必有right，但如果不是满二叉树，会有edge case要考虑。
        所以这里用到4个变量：
        下一层的开始节点head：相当于linked list的假头，这个head.next指向的是，下一层的开始节点
        当前层的当前遍历节点curr_level_node，以及下一层的当前遍历节点next_level_node
        has_next_level，一个flag，判断是否还有下一层，防止死循环，因为到最后一层的时候，head.next永远指向的是最后一层的第一个
        如果不判断是否是最后一层，则curr_level_node会无限的返回到head.next
    """
    def bfs_constant_space_any_tree(root):
        curr_level_node = root
        next_level_node = head = TreeLinkNode(-1)
        has_next_level = 0
        while curr_level_node:
            # 如果有left或者right，next_level_node.next需要先指向left然后指向right，以及挪动next_level_node
            if curr_level_node.left:
                next_level_node.next = curr_level_node.left
                next_level_node = next_level_node.next
                has_next_level = 1
            if curr_level_node.right:
                next_level_node.next = curr_level_node.right
                next_level_node = next_level_node.next
                has_next_level = 1
            # move on to the next on current level
            curr_level_node = curr_level_node.next
            if not curr_level_node and has_next_level:
                # 如果curr_level_node为None，即本层结束下层开始，curr_level_node从head.next开始
                # 而 next_level_node还是从这个head开始
                next_level_node = head
                curr_level_node = head.next
                has_next_level = 0

    def bfs_constant_space_complete_tree(root):
        # 对于某一个满二叉树node来说，如果不是leaf，那么必有left and right，而且node.left.next = node.right
        # 但是对于node.right.next来说，需要根据当前node.next来判断：如果node.next存在，那么node.right.next = node.next.left
        # 所以需要两个变量，一个记录当前层的开始节点level_start，另一个是当前层的遍历节点curr。
        level_start = root
        while level_start:
            curr = level_start
            while curr:
                if curr.left:
                    # 有left必有right
                    curr.left.next = curr.right
                if curr.right and curr.next:
                    # 有right，同时也有next，那么把right -> next.left
                    curr.right.next = curr.next.left
                curr = curr.next
            level_start = level_start.left

    def bfs_extra_space(root):
        queue = deque([root])
        while queue:
            size = len(queue)
            while size:
                size -= 1
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                # 如果queue空了，说明本层遍历结束，当前node的下一个为None
                node.next = queue[0] if size else None


def merge_two_binary_trees(t1, t2):
    """
    https://leetcode.com/problems/merge-two-binary-trees/submissions/
    """
    if t1 and t2:
        new_root = TreeNode(t1.val + t2.val)
        new_root.left = merge_two_binary_trees(t1.left, t2.left)
        new_root.right = merge_two_binary_trees(t1.right, t2.right)
        return new_root
    elif t1 is not None and t2 is None:
        return t1
    elif t1 is None and t2 is not None:
        return t2
    else:
        return None
