# -*- coding: utf-8 -*-

"""
图的基本表示方式：
1. Adjacent 二维 matrix[i][j]
    节点i到j不等于0表示相连，如果是加权图，对应的就是i->j的距离/权重/成本
    如果是无向图，矩阵的一半容量就浪费了，因为对角线对称。

2. Adjacent 链表
    类似于bucket，每一个slot对应的是一个node，后边指向的是这个node的所有相连node信息

3. 散列nested数组
    每个数组的元素是一个nested结构，包含了对应的相连的edge，比如[(n1, n2), (n2, n3)...]

4. 哈希map
    key就是某一个node，value就是一个hash set，存放的是相邻的node，适用于稀疏图

"""