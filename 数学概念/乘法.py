# -*- coding: utf-8 -*-


def multiply_strings(num1, num2):
    # https://leetcode.com/problems/multiply-strings/description/
    # 乘法，M*N位，最后结果最多有M+N位。同时，每一位i j的乘积，num1[i]*num2[j]，要考虑i和j所对应的数位
    # 比如 123 * 45，i=3 j=2 nums1[i] * num2[j] = 1*4 = 4 但还要考虑对应的位置i+j-1=4
    # 所以nums1[3] * num2[2]=4000，需要更新的是结果中i+j-1=4位置的数字
    if num1 == '0' or num2 == '0':
        return '0'
    m, n = len(num1), len(num2)
    res = [0] * (m + n) # 初始值均为0，用来存储最后结果每一位数字
    # 逆序遍历
    for i in xrange(m - 1, -1, -1):
        for j in xrange(n - 1, -1, -1):
            p = int(num1[i]) * int(num2[j])
            # 此时的p对应的数位是i+j+1
            sum = p + res[i + j + 1]
            # update res[i+j], res[i+j+1]
            res[i + j] += sum / 10  # 35/10=3
            res[i + j + 1] = sum % 10  # 35%10=5
    for i in xrange(len(res)): res[i] = str(res[i])
    if res[0] == '0':
        # 第一位为0，也就是M+N-1位个非0数字
        return ''.join(res[1:])
    return ''.join(res)


def complex_number_multiplication(a, b):
    # https://leetcode.com/problems/complex-number-multiplication/description/
    # 复数乘法，假定输入的format固定为 "x+yi"，x和y可能为负数，比如"-10+-2i"
    # 在python中 int('-10') = -10
    a = a[:-1].split('+')
    a1, a2 = int(a[0]), int(a[1])
    b = b[:-1].split('+')
    b1, b2 = int(b[0]), int(b[1])
    return '%d+%di' % (a1 * b1 - a2 * b2, a1 * b2 + a2 * b1)
