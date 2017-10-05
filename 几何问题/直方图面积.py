# -*- coding: utf-8 -*-


def largest_rectangle_histogram(heights):
    """
    https://leetcode.com/problems/largest-rectangle-in-histogram/description/
    给定一个数组，里面记录了每个直方图bar的高度，假设所有的直方图宽度为1，求出直方图最大的面积。

    维护一个单调递增的栈（栈内存元素的下标），比较栈顶（下标对应元素）与当前元素i
        如果当前元素i大于栈顶（下标对应元素）则入栈
        否则一直出栈，并逐个计算面积（取最大值），直到栈顶（下标对应元素）小于当前元素i

    其实可以理解为，对于当前高度i，如果它对目前为止找到的直方图（即存在于stack中的height index）的面积100%有贡献，
    也就是，它的高度比单调栈的top的高度相等甚至更高，那么stack中的直方图面积可以继续增加
    另一方面，如果没有贡献，即小于stack top高度，那么需要从stack顶端开始寻找，找到i可以贡献的点，也就是直到stack top <= i
    在这之后，i才会对新的stack中的直方图有贡献。
    """
    stack = list([])  # stack in non-decreasing order
    i = ma = 0
    n = len(heights)
    while i < n or stack:
        if not stack or (i < n and heights[stack[-1]] <= heights[i]):
            # 栈为空，或者top元素对应的height <= 当前i的height，满足递增，加入到stack中去
            stack.append(i)
            i += 1  # increasing
        else:
            # 栈不为空，或者新得到的height[i]，比栈顶的要小
            top = stack.pop()
            # 因为是单调递增，每次的top不会比上一次的top大，所以计算本次的直方图面积的时候，考虑本次的top作为高
            # 比如 如果stack = [10, 20] 第一次top=20，宽度为1，第二次top=10，宽度为2，之前的top=20不能全算进去
            h = heights[top]
            # 如果stack为空，也就是从0开始，宽度就等于i；否则，宽度=i-top-1（因为此时i本身不能算进直方图里面）
            w = i - stack[-1] - 1 if stack else i
            ma = max(ma, h * w)
    return ma


def parse_column(row, run_sum_col):
    # 给定一行数据，和之前的running column sum，更新running column sum in place
    for j, val in enumerate(row):
        val = int(val)
        # 如果每某一列有gap，即比如1 1 0，那么到0的时候，上边的两个1就不能算进去了
        run_sum_col[j] = run_sum_col[j] + val if val != 0 else 0


def max_rectangle(matrix):
    """
    https://leetcode.com/problems/maximal-rectangle/description/
    给定一个01 matrix，找到里面1所能够组成的矩形的最大面积
    这道题目类似于Largest Rectangle in Histogram
    每一个矩形的bottom都是1。如果把每一行当做是底，找到用这个底能组成的最大的矩形面积。

    所以可以给每一行的cell构建一个直方图，相当于是running sum of previous columns，利用逐层累加数组来表示矩阵。
    之后对于每一层的"直方图"，调用largest_rectangle_histogram当做是API，求得本层的最大矩形直方图面积，然后更新全局最大值。

    Edge case就是，如果每一列有gap，即比如1 1 0，那么到0的时候，上边的两个1就不能算进去了
    """
    ma = 0
    if matrix and matrix[0]:
        running_h = [0] * len(matrix[0])
        for row in matrix:
            # 计算出 running sum of previous columns
            parse_column(row, running_h)
            ma = max(ma, largest_rectangle_histogram(running_h))
    return ma


def maximum_square(matrix):
    """
    https://leetcode.com/problems/maximal-square/description/
    找到一个只包含01的矩阵中，能够形成的最大的正方形面积，比如下图，面积为4
    1 0 1 0 0
    1 0 1 1 1
    1 1 1 1 1
    1 0 0 1 0

    类似于max_rectangle的解法，但是此时限定条件为，必须可以组成一个正方形。
    暴力解法：从顶点开始，把它当做是正方形的top-left-point，也就是查看这个点开始，能够组成的正方形的最大边长为多少，即最大面积
    解法2：类似于max rectangle的解法：对于每一行，求出每一列的累加和，然后对这个累加和数组进行判断：
        对于每个位置的累加和k，如果能够从两边extend，找到连续k-1个累加和，满足>=k，也就相当于是，找到了一个边长为k的正方形
        那么就找到了一种可能的edge，用来更新全局edge，最后返回的是全局edge的平方
        时间复杂度：M行N列，每一行处理N列，O(M*N)，之后，每一行的column累加和需要寻找可能的左右边界，每次O( N * min(M, N))
            假设 M = N，那么最后时间复杂度为O(N^3)，额外空间复杂度O(N)
    解法3：DP，时间复杂度O(N^2)
    """
    def find_max_edge(columns):
        max_edge = 0
        for i, edge in enumerate(columns):
            if 0 < edge <= len(columns):
                # 如果edge比column的长度还大，比如8行5列，但是某一列的累加和为6，比5大，不可能组成正方形
                edge_count = 1
                j = i + 1
                # 首先向右边走
                while j < len(columns) and edge_count < edge <= columns[j]:
                    j += 1
                    edge_count += 1
                # 接着向左边走
                j = i - 1
                while j >= 0 and edge_count < edge <= columns[j]:
                    j -= 1
                    edge_count += 1
                if edge_count == edge:
                    max_edge = max(max_edge, edge)
        return max_edge
    max_edge_global = 0
    if matrix and matrix[0]:
        running_h = [0] * len(matrix[0])
        for row in matrix:
            parse_column(row, running_h)
            max_edge_global = max(max_edge_global, find_max_edge(running_h))
    return max_edge_global * max_edge_global


def test_matrix():
    matrix = [
        ["10100","10111","11111","10010"],
        ["1010", "1011", "1011", "1111"]
    ]
    for m in matrix:
        print maximum_square(m)
