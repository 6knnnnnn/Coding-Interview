# -*- coding: utf-8 -*-


def diagonal_matrix_print(matrix):
    """
    Input:
    1 2 3
    4 5 6
    7 8 9
    Print Output:
    3, 2 6, 1 5 9, 4 8, 7
    用一个queue记录(i, j, value)，横竖坐标+值，每一个对角线从left-top -> right-bottom 依顺序FIFO记录
    queue中每个元素出从head出队列，把对应的左边的元素加入到tail，如果有的话（即j>0）
    特殊情况是，如果这个元素是在最右边，即j=max_column，那么还需要记录下边的元素，如果有的话（即i>0）
    """


def diagonal_traverse(matrix):
    """
    https://leetcode.com/problems/diagonal-traverse/description/
    Input:
    [ 1, 2, 3 ],
    [ 4, 5, 6 ],
    [ 7, 8, 9 ]
    Output:  [1,2,4,7,5,3,6,8,9]，即旋转对角线打印
    """
