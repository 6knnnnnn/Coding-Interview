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
    自顶向上，找到对应结果中的index，比如 [4, 5, 3]的index都是0，[2]是1，[1]是2，这样的index其实就是
    这道题目不应该用暴力"剪枝"的做法，就是剪完了叶子后，再从新剪枝，因为只是说 as if 感觉 而不是真的剪枝
    """

    @staticmethod
    def dfs(root):
        # 这道题目关键点是，DFS的时候，节点的高度，是由"最底层"的叶子节点开始的，因为他们的index为0，然后自底向上+1
        def add_to_level(results, node, curr_level):
            if not node:
                # 为None，说明上一层传过来的节点可能为叶子节点，返回-1
                return -1
            if len(results) < curr_level:
                # 当前level超过了results所包含的level，新建一个
                results.append(list([]))
            left = add_to_level(results, node.left, curr_level+1)
            right = add_to_level(results, node.right, curr_level+1)
            # 如果当前node为最底（开始）层的叶子节点，那么left=right=-1，所以他们对应的index就是-1+1=0
            # 否则当前node为当前层的"叶子"节点，加入到对应的index结果里面
            index = max(left, right) + 1
            results[index].append(node.val)
            # 将当前node的index返回给上一级，也就是它的parent
            # 那么parent的在结果里面的位置就是index+1（需要取最大值，因为可能parent有两个child，找其中最大的index）
            return index
        results = list([])
        add_to_level(results, root, 1)
        return results

    @staticmethod
    def bfs(root):
        """
        一个hash map，记录child->parent关系，以及parent的孩子节点数量，一个leaf target queue，本层需要处理的"叶子"节点。
        每次遍历所有的leaf target queue，找到本层叶子节点的parent并更新它的child num减1，如果parent变成了下一层的叶子节点
        即parent child num = 0，放到queue里面
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
                # 如果顺序有影响，需要用queue，保持顺序，没有影响，可以用list，存放的是逆序的
                results.append(deque([]))
                while size:
                    size -= 1
                    leaf_child = curr_leaf_queue.popleft()
                    results[-1].appendleft(leaf_child.val)
                    if leaf_child not in child_parent_map:
                        # 特殊情况，此时的leaf为root，此时child_parent_map为空，curr_leaf_queue只有root，可以返回最后的结果
                        return results
                    parent_node, child_num = child_parent_map[leaf_child]
                    child_parent_map[leaf_child][1] -= 1
                    if child_num == 0:
                        # 当前child leaf被剪枝后，parent也要变成leaf了
                        curr_leaf_queue.append(parent_node)
                        child_parent_map.pop(leaf_child)
        return results


