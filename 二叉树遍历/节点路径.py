# -*- coding: utf-8 -*-

from collections import deque


class Diameter(object):
    def __init__(self):
        self.diameter = 0

    def bottom_up_get_height(self, root):
        """
        优化解法：Bottom-up 遍历收集信息，跟暴力解法类似，但是用一个全局变量记录最大的diameter
        先遍历到底即叶子节点，然后自底向上更新全局变量，分别跟左右节点的height之和比较找最大
        关键点是：1）每次先DFS取得左右节点的height，再更新diameter；2）返回的是左右子树最大的height给上级；
        """
        if not root:
            return 0
        left = self.bottom_up_get_height(root.left)
        right = self.bottom_up_get_height(root.right)
        self.diameter = max(self.diameter, left + right)
        return 1 + max(left, right)

    def diameter_binary_tree(self, root):
        """
        https://leetcode.com/problems/diameter-of-binary-tree/description/
        The diameter of a binary tree is the length of the longest path between any two nodes in a tree.
        This path may or may not pass through the root. Example below: Return 3 [4,2,1,3] or [5,2,1,3].
              1
             / \
            2   3
           / \
          4   5
        暴力解法：对于每一个node，找到对应左右子树的height，相加之和再加上1（当前node），然后分别和左右子树的diameter比较，找出三者中最大
        """
        self.diameter = 0
        self.bottom_up_get_height(root)
        return self.diameter


def binary_tree_paths(root):
    """
    https://leetcode.com/problems/binary-tree-paths/description/
    给定一个root，返回所有的root-to-leaf-path为一个list，比如 ["1->2->5", "1->3"]
       1
     /   \
    2     3
     \
      5
    """
    def dfs(node, res_list, curr_path):
        # DFS，记录之前的path，直到碰见leaf node为止
        if node:
            curr_path = "%s->%s" % (curr_path, node.val)
            if not node.left and not node.right:
                res_list.add(curr_path)
            else:
                dfs(node.left, res_list, curr_path)
                dfs(node.right, res_list, curr_path)

    def bfs(node):
        # BFS，每次queue记录的元素为（node，curr_path），跟DFS一个意思
        res_list = list([])
        if node:
            queue = deque([(node, "")])
            while queue:
                node, curr_path = queue.popleft()
                curr_path = "%s->%s" % (curr_path, node.val) if curr_path else str(node.val)
                if not node.left and not node.right:
                    res_list.append(curr_path)
                if node.left:
                    queue.append((node.left, curr_path))
                if node.right:
                    queue.append((node.right, curr_path))
        return res_list
    return bfs(root)


def sum_root_to_leaf_number(root):
    """
    https://leetcode.com/problems/sum-root-to-leaf-numbers/description/
    每个节点表示一个digit，值域为[0, 9]，找到所有root-leaf-path，然后把所有path的数值相加
    其实就是binary_tree_path的变体
    """
    if not root:
        return 0
    queue, res = deque([(root, root.val)]), 0
    while queue:
        n, value = queue.popleft()
        if not n.left and not n.right:
            res += value  # leaf node, add to result
        if n.left:
            queue.append((n.left, value * 10 + n.left.val))
        if n.right:
            queue.append((n.right, value * 10 + n.right.val))
    return res


def binary_tree_maximum_path_sum(root):
    """
    https://leetcode.com/problems/binary-tree-maximum-path-sum/description/
    找到最大的路径和，这个路径可以是任意的parent-child-path，不一定是root-leaf-path
    A path is defined as any sequence of nodes from some starting node to any node
    in the tree along the parent-child connections.
    有点类似于diameter
    """
