# -*- coding: utf-8 -*-

# 序列化问题需要考虑两点：用什么来当分隔符和None字符，用什么遍历顺序来序列化和反序列化。
from collections import deque
from utility.entity import TreeNode


class SerializeBT(object):
    index = 0
    # https://leetcode.com/problems/serialize-and-deserialize-binary-tree/description/

    def dfs_serialize(self, str_list, node):
        if node:
            # 这里用的pre-order遍历方式
            str_list.append(str(node.val))
            self.dfs_serialize(str_list, node.left)
            self.dfs_serialize(str_list, node.right)
        else:
            str_list.append("#")

    def serialize(self, root):
        str_list = []
        self.dfs_serialize(str_list, root)
        return ','.join(str_list)

    def dfs_deserialize(self, str_list):
        val = str_list[self.index]
        self.index += 1 # 及时更新index
        if val != '#':
            node = TreeNode(int(val))
            node.left = self.dfs_deserialize(str_list)
            node.right = self.dfs_deserialize(str_list)
            return node
        return None

    def deserialize(self, tree_str):
        # 此时index相当于是一个iterator，记录了对应的当前str值
        self.index = 0
        str_list = tree_str.split(",")
        return self.dfs_deserialize(str_list)


class SerializeBST(object):
    # https://leetcode.com/problems/serialize-and-deserialize-bst
    # 跟Deserialize Binary Tree相比，BST的特殊性？Preorder之后，root-left-right，所有left小于root，right反之
    # 所以序列化的时候直接用pre-order，而且不用考虑None的情况；反序列化的时候，第一个val就是root
    # 之后所有比root小的，都是left subtree的节点，反之都是right subtree的节点
    # 最坏的情况O(N^2) when tree unbalanced, average O(N logN)

    def serialize(self, root):
        if not root:
            return ""
        res = list([])
        s = list([root])
        # preorder:right FILO, left LIFO
        while s:
            n = s.pop()
            res.append(str(n.val))
            if n.right:
                s.append(n.right)
            if n.left:
                s.append(n.left)
        return ','.join(res)

    def dfs_deserialize(self, queue):
        if not queue:
            return None
        root = TreeNode(queue.popleft())
        left_queue = deque([])
        while queue and queue[0] < root.val:
            left_queue.append(queue.popleft())
        root.left = self.dfs_deserialize(left_queue)
        root.right = self.dfs_deserialize(queue)
        return root

    def deserialize(self, data):
        if not data:
            return None
        data = data.split(",")
        q = deque([int(d) for d in data])
        return self.dfs_deserialize(q)


def subtree_of_another_tree(tree1, tree2):
    """
    https://leetcode.com/problems/subtree-of-another-tree/description/
    结构和node值一样，且不能有子树，比如第二个和第一个是subtree，但是和第三个不是
         3          4           3
        / \        / \         / \
       4   5      1   2       4   5
      / \                    / \
     1   2                  1   2
                               /
                              6
    M N 为两棵树的节点数
    解法1：纯暴力，每次从tree1的root开始遍历，看是否能跟tree2匹配，时间复杂度O(M*N)
    解法2：序列化两棵树，用KMP来看较短的是否是较长的substring，时间复杂度O(M+N)，要用额外空间M+N
    """
