# -*- coding: utf-8 -*-


def multiply_strings(num1, num2):
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
    for i in xrange(len(res)-1):
        # 变成string
        res[i] = str(res[i])
    return ''.join(res[1:]) if res[0] == '0' else ''.join(res)
