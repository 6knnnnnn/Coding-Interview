# -*- coding: utf-8 -*-


def rotate_image(matrix):
    """
    https://leetcode.com/problems/rotate-image
    基本思路就是，对于任意一个坐标[r, c]，旋转九十度之后的坐标为[c, n-1-r]，n即矩阵维度
    旋转=转置+上下翻转后，所以可以让任意坐标[r, c]先转置为[c, r]，在上下翻转为[c, n-1-r]
    """
    if matrix is None:
        return
    n = len(matrix)
    for i in xrange(n):  # Transpose
        for j in xrange(i, n):
            # Do the swap with (i,j) and (j,i)
            matrix[j][i], matrix[i][j] = matrix[i][j], matrix[j][i]
    for i in xrange(n):  # flip the matrix horizontally
        for j in xrange(n / 2):
            # Do the swap with (i,j) and (i,n-1-j)
            matrix[i][j], matrix[i][n - 1 - j] = matrix[i][n - 1 - j], matrix[i][j]


def spiral_matrix(matrix):
    """
    https://leetcode.com/problems/sparse-matrix-multiplication/description/
    维持四个变量 row begin, col end, row end, col begin，每次遍历后更新
    row begin 行，从col begin -> col end
    col end   列，从row begin -> row end
    row end   行，从col end -> col begin 逆序走
    col begin 列，从row end -> row begin 逆序走
    """
    res = list([])
    if matrix:
        row_begin = col_begin = 0
        row_end, col_end = len(matrix)-1, len(matrix[0])-1
        while row_begin <= row_end and col_begin <= col_end:
            # 最上一行向右走
            for c in xrange(col_begin, col_end+1):
                res.append(matrix[row_begin][c])
            row_begin += 1
            # 最右一列向下走
            for r in xrange(row_begin, row_end+1):
                res.append(matrix[r][col_end])
            col_end -= 1
            if row_begin <= row_end:
                # 最下一行向左走
                for c in xrange(col_end, col_begin-1, -1):
                    res.append(matrix[row_end][c])
            row_end -= 1
            if col_begin <= col_end:
                # 最左一列向上走 xrange[left, right) right is exclusive
                for r in xrange(row_end, row_begin-1, -1):
                    res.append(matrix[r][col_begin])
            col_begin += 1
    return res


M = [[1,2,3],[4,5,6],[7,8,9]]

print spiral_matrix(M)


def spiral_matrix_generator(n):
    """
    https://leetcode.com/problems/spiral-matrix-ii/description/
    给定数字N，生成一个N*N的矩阵，满足上边的spiral遍历，其实一个道理，用一个全局计数
    """
    matrix = [ [0]*n for _ in xrange(n) ]
    return matrix

