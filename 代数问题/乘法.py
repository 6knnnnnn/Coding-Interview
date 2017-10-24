# -*- coding: utf-8 -*-


def multiply_strings(num1, num2):
    # https://leetcode.com/problems/multiply-strings/description/
    # 乘法，M*N位，最后结果最多有M+N位。同时，每一位i j的乘积，num1[i]*num2[j]，要考虑i和j所对应的数位
    if num1 == '0' or num2 == '0':
        return '0'
    m, n = len(num1), len(num2)
    res = [0] * (m + n) # 初始值均为0，用来存储最后结果每一位数字
    # 逆序遍历
    for i in xrange(m - 1, -1, -1):
        for j in xrange(n - 1, -1, -1):
            # 此时i*j对应的数位是i+j+1
            res[i + j + 1] += int(num1[i]) * int(num2[j])
            # 进位 i+j+1 -> i+j，即当前i+j+1的前一位，以及自己位的数字
            res[i + j] += res[i + j + 1] / 10  # +(35/10=3)
            res[i + j + 1] %= 10  # 35%10=5
    for i in xrange(len(res)):
        res[i] = str(res[i])
    # 第一位为0
    return ''.join(res[1:]) if res[0] == '0' else ''.join(res)


def multiply_string_two_pass(num1, num2):
    # 上一种解法一致，不过先做乘法，在做进位
    # 123 * 45 = [0, 0, 5, 10, 15] + [0, 4, 8, 12, 0] = [0, 4, 13, 22, 15]
    # 之后再进位，不过不需要处理res[0]，最高位，不可能为10
    # 如果某一位大于10，该位对除以10的结果加到下一位上去，同时该位%10，比如32，下一位+3，该位%10=2
    if num1 == '0' or num2 == '0':
        return '0'
    m, n = len(num1), len(num2)
    res = [0] * (m + n)
    for i in xrange(m - 1, -1, -1):
        for j in xrange(n - 1, -1, -1):
            res[i + j + 1] += int(num1[i]) * int(num2[j])
    for i in xrange(len(res)-1, 0, -1):
        # 进位
        res[i-1] += res[i] / 10
        res[i] %= 10
    for i in xrange(len(res)-1): # 变成string
        res[i] = str(res[i])
    return ''.join(res[1:]) if res[0] == '0' else ''.join(res)


def complex_number_multiplication(a, b):
    # https://leetcode.com/problems/complex-number-multiplication/description/
    # 复数乘法，假定输入的format固定为 "x+yi"，x和y可能为负数，比如"-10+-2i"
    # 在python中 int('-10') = -10
    a = a[:-1].split('+')
    a1, a2 = int(a[0]), int(a[1])
    b = b[:-1].split('+')
    b1, b2 = int(b[0]), int(b[1])
    return '%d+%di' % (a1 * b1 - a2 * b2, a1 * b2 + a2 * b1)


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
