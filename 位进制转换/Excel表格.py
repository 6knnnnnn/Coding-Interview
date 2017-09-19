# -*- coding: utf-8 -*-
# 1 -> A，2 -> B，3 -> C ... 26 -> Z，27 -> AA，28 -> AB


def excel_sheet_column_title(n):
    """
    https://leetcode.com/problems/excel-sheet-column-title/description/
    给定一个数，返回对应的excel表格列名
    n 拆分成两个部分，n/26 * ? + n % 26
    ABCD＝A×26³＋B×26²＋C×26¹＋D＝1×26³＋2×26²＋3×26¹＋4 = 19010
    ZZZZ＝Z×26³＋Z×26²＋Z×26¹＋Z＝26×26³＋26×26²＋26×26¹＋26 = 475254
    """
    cols = ""
    while n:
        # 逆序，先生成最小的title，加入到结果中去，然后找次小的
        # (n-1)%26 是因为我们想到得到的是[0, 25]
        x = (n - 1) % 26
        # 'A' = 65, 把x转化为ASCII
        cols = chr(x + 65) + cols
        # 更新n
        n = (n - 1) / 26
    return cols


def excel_sheet_column_number(column):
    """
    https://leetcode.com/problems/excel-sheet-column-number/description/
    Base 26, BCA = 2*26^2 + 3*26^1 + 1*26^0
    """
    number, length = 0, len(column)-1
    for c in column:
        digit = ord(c) - 64
        number += digit * (26**length)
        length -= 1
    return number


for _ in [26, 27, 28, 1431]:
    print _, excel_sheet_column_title(_)

