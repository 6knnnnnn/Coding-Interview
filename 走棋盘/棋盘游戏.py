# -*- coding: utf-8 -*-


def valid_sudoku(board):
    """
    https://leetcode.com/problems/valid-sudoku/description/
    数独游戏规则：每一行，每一列，每一个cube（3x3的小格子）都不能有重复的数字
    暴力解法：对于每一行和每一列以及每一个cube，生成一个tuplr，放到list里面
    最后把list转换成为一个hash set，根据hash set的大小判断是否存在重复的记录，时间空间 O (M*N)
    """
    seen = []
    # 这里面初始化一个list而非hash set，其实本质上是一样的
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if c != '.':
                seen += [(c, j), (i, c), (i / 3, j / 3, c)]
    return len(seen) == len(set(seen))

