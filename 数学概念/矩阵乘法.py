# -*- coding: utf-8 -*-


def matrix_multiplication(A, B):
    # 暴力解法，时间复杂度O(MNP)
    if not A or not B:
        return None
    rowA, colA = len(A), len((A[0]))
    rowB, colB = len(B), len(B[0])
    if colA != rowB:
        return None
    # A=M行N列，B=N行P列，结果为M行P列
    C = [[0] * colB for _ in xrange(rowA)]
    for i in xrange(rowA):
        for j in xrange(colB):
            # A的行乘以B的列的sum
            for k in xrange(rowB):
                # k表明colA和rowB必须相等
                C[i][j] += A[i][k]*B[k][j]
    return C


def test1():
    a = [[1,2], [3,4], [5,6], [7,8]]
    b = [[1,2,3,4], [5,6,7,8]]
    print matrix_multiplication(a, b)


test1()


def sparse_matrix_multiplication(A, B):
    # https://leetcode.com/problems/sparse-matrix-multiplication
    # 这道题跟上边的矩阵相乘不同的时，先考虑B[N][0..P-1]中所有和A[M][N]相乘的情况
    if not A or not B:
        return None
    rowA, colA = len(A), len((A[0]))
    rowB, colB = len(B), len(B[0])
    C = [[0] * colB for _ in xrange(rowA)]
    for i in xrange(rowA):
        # 这时候先考虑B的对应行的情况，也就是所有需要和A[i][k]相乘的B中的元素
        for k in xrange(rowB):
            if A[i][k]: # 只有在A不为0的时候，才考虑这些B的元素
                for j in xrange(colB):
                    # B为不为0的时候均无所谓
                    C[i][j] += A[i][k] * B[k][j]
    return C


def sparse_matrix_multiplication_bucket(A, B):
    """
    用一个hash table bucket记录B矩阵的非0元素的信息，
        key = row num, bucket = 另一个hash table，key=非0元素的列，value就是对应的值
    """
    if not A or not B: return None
    rowA, colA, colB = len(A), len(A[0]), len(B[0])
    C = [[0] * colB for _ in xrange(rowA)]
    table_b = {}
    for i, row in enumerate(B):
        table_b[i] = {}  # build map for B, key=colB
        for j, valB in enumerate(row):
            if valB:
                table_b[i][j] = valB
    for i, row in enumerate(A):
        for j, valA in enumerate(row):
            if valA:
                # 这样子只有当A[i][j] B[j][k]均不为0的时候，才相乘
                for k, valB in table_b[j].iteritems():
                    C[i][k] += valA * valB
    return C
