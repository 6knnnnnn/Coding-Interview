# -*- coding: utf-8 -*-


def search_in_matrix(matrix, target):
    """
    https://leetcode.com/problems/search-a-2d-matrix/description/
    每一行都是排好序的，且每一行的第一个数字总比之前一行的最后一个数字大
    [1,   3,  5,  7]
    [10, 11, 16, 20]
    [23, 30, 34, 50]
    暴力解法就是走格子，从最小或者最大值开始走，时间O(M+N)
    二分O(log(M+N))，这里可以把整个matrix当做一维数组来看，升序排列
    """
    if matrix and target is not None:
        rows, cols = len(matrix), len(matrix[0])
        # high->the last one
        low, high = 0, rows * cols - 1
        # same as binary search
        while low <= high:
            mid = (low + high) >> 1
            # 关键点：对于任意的index, index/cols = 行数, index%cols = 列数
            num = matrix[mid / cols][mid % cols]
            if num == target:
                return True
            elif num < target:
                low = mid + 1
            else:
                high = mid - 1
    return False


def search_in_matrix_2_linear(matrix, target):
    """
    https://leetcode.com/problems/search-a-2d-matrix-ii/description/
    [1,   4,  7, 11, 15]
    [2,   5,  8, 12, 19]
    [3,   6,  9, 16, 22]
    [10, 13, 14, 17, 24]
    [18, 21, 23, 26, 30]
    行和列分别排好序，从top right开始向bottom left走，如果找到了matrix[i][j]=target则结束
    如果比target大，说明当前j列的下边的行，都比target大，此时向左走
    如果比target小，说明当前i行的做边的列，都比target小，此时向下走
    时间复杂度O(M+N)，此题应该没有binary search的做法
    """
    if matrix and len(matrix) > 0:
        i, j = 0, len(matrix[0]) - 1  # top-right
        while i < len(matrix) and j >= 0:
            if target == matrix[i][j]:
                return True
            # if bigger, move to next row
            if target > matrix[i][j]:
                i += 1
            # if smaller, move to prev col
            else:
                j -= 1
    return False


def kth_smallest_element_in_sorted_matrix(matrix, k):
    """
    https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/
    给定一个行和列分别排好序的N x N矩阵，跟上面的一样，找到第K小的元素
    这道题目可以用heap来解决，类似于merge k sorted array，O(N)空间，O(K*logN)时间，K<=N^2
    二分搜索法？
    把这个矩阵当做是一个区间，每次找到区间内的中值mid
    计算出有多少个元素小于这个mid，然后根据元素个数count来更新区间的值域
    """
    if not matrix:
        return None
    n = len(matrix)
    low, high = matrix[0][0], matrix[-1][-1]
    while low < high:
        mid = (high + low) >> 1
        count = 0
        j = n - 1
        # 看矩阵中有多少<=mid
        for i in xrange(0, n):
            # 对于行，找到所有<= mid的元素个数j+1
            while j >= 0 and matrix[i][j] > mid:
                j -= 1
            count += j + 1
            # if there are less than k in [i,j] <= mid
        # mid is too small, update low so increase mid
        if count < k:
            low = mid + 1
        # if there are greater than k in [i,j] <= mid
        # mid is too big, update high so decrease mid
        else:
            high = mid
    return low
