# -*- coding: utf-8 -*-


class NestedWeightSum(object):
    # https://leetcode.com/problems/nested-list-weight-sum/description/
    # top-down depth/weight 顺序
    # 其实就是类似于graph level traversal
    @staticmethod
    def dfs(nested_list):
        def dfs_helper(node, depth, dMap):
            if depth not in dMap:
                dMap[depth] = 0
            if node.isInteger():
                dMap[depth] += node.getInteger()
            else:
                for n in node.getList():
                    dfs_helper(n, depth + 1, dMap)
        dMap = {} # 记录每个depth对应的和x，最后的加权和就是所有x和对应depth的乘积的累加
        result = 0
        for node in nested_list:
            dfs_helper(node, 1, dMap)
        for num, depth in dMap.items():
            result += num * depth
        return result

    @staticmethod
    def bfs(nested_list):
        if not nested_list:
            return 0
        queue = deque([])
        result = 0
        for n in nested_list:
            queue.append((n, 1))
        while queue:
            node, d = queue.popleft()
            if node.isInteger():
                result += d * node.getInteger()
            else:
                for i in node.getList():
                    queue.append((i,d+1))
        return result


class NestedWeightSumReverse(object):
    # https://leetcode.com/problems/nested-list-weight-sum-ii/description/
    # bottom-up depth/weight 逆序
    # 跟top-down不同的是，需要找到最大的max depth
    # 最后返回的时候，用max depth - current depth 就是对应的weight了
    @staticmethod
    def dfs(nested_list):
        def dfs_helper(node, level, dMap):
            dMap[-1] = max(dMap[-1], level)
            if level not in dMap:
                dMap[level] = 0
            if node.isInteger():
                dMap[level] += node.getInteger()
            else:
                for n in node.getList():
                    dfs_helper(n, level + 1, dMap)
        dMap = {-1: 0} # -1纪录最大的max depth
        result = 0
        for node in nested_list:
            dfs_helper(node, 1, dMap)
        max_depth = dMap.pop(-1)
        for num, depth in dMap.items():
            result += (max_depth - depth + 1) * num
        return result

    @staticmethod
    def bfs(nested_list):
        # 跟top-down一样，只是多了一次遍历queue，找到最大的max depth
        if not nested_list:
            return 0
        queue = deque([])
        result = 0
        for n in nested_list:
            queue.append((n, 1))
        max_depth = -1
        queue2 = deque([])
        while queue:
            queue2.append(queue.popleft())
            node, d = queue2[-1]
            new_depth = d + 1
            if not node.isInteger():
                for i in node.getList():
                    max_depth = max(max_depth, new_depth)
                    queue.append((i, new_depth))
        while queue2:
            node, d = queue2.popleft()
            if node.isInteger():
                result += (max_depth-d+1) * node.getInteger()
            else:
                for i in node.getList():
                    queue2.append((i, d+1))
        return result
