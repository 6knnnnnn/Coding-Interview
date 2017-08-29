# -*- coding: utf-8 -*-

"""
收集并返回子节点信息给上级进行决策，然后继续递归给上上级。
如果top-bottom过于暴力：每次top节点需要重复遍历，不同的top会有不同的结果（因为都是相对值），可能会重复遍历导致O(N^2)时间复杂度。
返回的左右子树信息可能包括：最值，均值，值域，包含节点个数，高度，而且左右子树返回信息结构一致。
为什么是后序遍历？因为需要根据左右字数的返回信息来判断，root返回的是什么信息，所以后序。
"""

from collections import deque


class FindLeavesBinaryTree(object):
    """
    https://leetcode.com/problems/find-leaves-of-binary-tree/description/
    收集到树的信息，"感觉"就像是，一层一层的减掉叶子节点后，再次把新的叶子节点减掉，最后返回的是 list of list
          1
         / \
        2  3
       / \
      4  5      返回：[[4, 5, 3], [2], [1]]
    这道题目不应该用暴力"剪枝"的做法，就是剪完了叶子后，再从新剪枝，因为只是说 as if 感觉 而不是真的剪枝
    """

    @staticmethod
    def dfs(root):
        # 这道题目关键点是，DFS的时候，节点的高度，是由"最底层"的叶子节点开始的
        def add_to_level(results, node, curr_level):
            if not node:
                # 为None，说明上一层传过来的节点可能为叶子节点，返回-1
                return -1
            if len(results) < curr_level:
                # 当前level超过了results所包含的level，新建一个
                results.append(list([]))
            left = add_to_level(results, node.left, curr_level+1)
            right = add_to_level(results, node.right, curr_level+1)
            index = max(left, right) + 1
            results[index].append(node.val)
            return index
        results = list([])
        add_to_level(results, root, 1)
        return results

    @staticmethod
    def bfs(root):
        """
        用一个hash map，记录child->parent关系，
        当前level，从树的bottom开始为0；一个queue，表示本层不需要处理的节点，以及parent所剩下的未被处理的孩子节点的个数
        另外一个leaf node queue，本层需要处理的"叶子"节点
        每次遍历所有的leaf node queue，找到
        """
        results = list([])
        if root:
            stack, curr_leaf_queue, child_parent_map = list([root]), deque([]), dict([])
            while stack:
                # 先遍历一次所有节点，预处理为之后做准备
                node = stack.pop()
                if not node.left and not node.right:
                    curr_leaf_queue.append(node)
                else:
                    # 至少有一个孩子节点
                    parent = [node, 2] if node.left and node.right else [node, 1]
                    if node.left:
                        child_parent_map[node.left] = parent
                        stack.append(node.left)
                    if node.right:
                        child_parent_map[node.right] = parent
                        stack.append(node.right)
            while child_parent_map or curr_leaf_queue:
                # 开始新的一层，如果curr_leaf_queue不为空但是child_parent_map为空
                # 说明最后剩下的是root节点了，因为root没有parent
                size = len(curr_leaf_queue)
                # 如果顺序有影响，需要用queue，保持顺序，否则list存放的是逆序的
                results.append(deque([]))
                while size:
                    size -= 1
                    leaf_child = curr_leaf_queue.popleft()
                    results[-1].appendleft(leaf_child.val)
                    if leaf_child not in child_parent_map:
                        # 特殊情况，此时的leaf为root，此时child_parent_map为空，curr_leaf_queue只有leaf，可以返回最后的结果
                        return results
                    parent_node, child_num = child_parent_map[leaf_child]
                    if child_num == 1:
                        # 只有一个child，说明当前child leaf被剪枝后，parent也要变成leaf了
                        curr_leaf_queue.append(parent_node)
                        child_parent_map.pop(leaf_child)
                    else:
                        # 有两个child，这里面-1
                        child_parent_map[leaf_child][1] -= 1
        return results


