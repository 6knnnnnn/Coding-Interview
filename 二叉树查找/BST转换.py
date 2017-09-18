# -*- coding: utf-8 -*-

from utility import TreeNode


class ArrayNode(object):
    # 被二分法的BFS来用
    def __init__(self, start, end, tree_node):
        self.start = start
        self.end = end
        self.mid = (self.start + self.end) >> 1
        self.tree_node = tree_node

    def get_all(self):
        return self.start, self.end, self.mid, self.tree_node


class SortedArrayToBST(object):
    # 要求返回的是平衡二叉树，所以需要用到二分法，时间复杂度O(N)，空间也是O(N)，因为最后的解空间为O(N)
    @staticmethod
    def dfs_solution(nums):
        def dfs(nums, start, end):
            if not nums or start > end:
                return None
            if start == end:
                return TreeNode(nums[start])
            mid = (start + end) / 2
            root = TreeNode(nums[mid])
            root.left = dfs(nums, start, mid - 1)
            root.right = dfs(nums, mid + 1, end)
            return root

        return dfs(nums, 0, len(nums) - 1)

    @staticmethod
    def bfs_solution(nums):
        # 其实就是用了stack来模拟recursion
        if not nums:
            return None
        root = TreeNode(nums[(len(nums)-1) >> 1])
        stack = list([ArrayNode(0, len(nums)-1, root)])
        while stack:
            array_node = stack.pop()
            start, end, mid, tree_node = array_node.get_all()
            if mid-1 >= start:
                tree_node.left = TreeNode(nums[(mid-1+start) >> 1])
                stack.append(ArrayNode(start, mid-1, tree_node.left))
            if mid + 1 <= end:
                tree_node.right = TreeNode(nums[(mid+1+end) >> 1])
                stack.append(ArrayNode(mid + 1, end, tree_node.right))
        return root


class SortedListToBST(object):
    # 其实跟sorted array一个道理，如果空间允许的话，把所有linked list转化为一个array即可
    # 如果不能转换，那只能暴力解法，时间复杂度O(N^2)
    @staticmethod
    def dfs_solution(head):
        def dfs(head, tail):
            root = None
            if head and head != tail:
                s = f = head
                while f != tail and f.next != tail:
                    # 快慢指针，找到中点，适用于许多需要linked list partition的问题
                    s, f = s.next, f.next.next
                root = TreeNode(s.val)
                root.left = dfs(head, s)
                root.right = dfs(s.next, tail)
            return root

        return dfs(head, None)
