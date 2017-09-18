# -*- coding: utf-8 -*-

"""
图的基本表示方式：
1. Adjacent matrix
    matrix[i][j]，即节点i到j不等于0表示相连，如果是加权图，对应的就是i->j的距离/权重/成本
    如果是无向图，矩阵的一半容量就浪费了，因为对角线对称。

2. Adjacent list
    类似于bucket，每一个slot对应的是一个node，后边指向的是这个node的所有相连node信息

3. Edge list
    每个数组的元素是一个nested结构，包含了对应的相连的edge，比如[(n1, n2), (n2, n3)...]

图是否有环？看是否存在back edge，也就是之前遍历过的节点

"""