# -*- coding: utf-8 -*-


def number_of_islands(matrix):
    # https://leetcode.com/problems/number-of-islands/description/
    # 用一个DFS方法，因为只是01 moveToCell，把所有遍历过的1变成别的flag比如2
    # 这样之后还可以把输入matrix还原。如果是变成0，无法还原
    def sink(lands, i, j):
        if 0 <= i < len(lands) and 0 <= j < len(lands[0]) and lands[i][j] == '1':
            lands[i][j] = '#'
            for k in [(i+1, j),(i-1, j), (i, j+1), (i, j-1)]:
                sink(lands, k[0], k[1])
    total = 0
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[i])):
            if matrix[i][j] == '1':
                # 找到一个新的岛屿，用DFS sink这个岛，之后不会再次遍历这个岛了，也就是total+1只出现一次
                sink(matrix, i, j)
                total += 1
    # 如果最后需要recover matrix，把所有#变为1
    return total


def islandsArea(matrix):
    # 计算所有island的面积
    def sink(lands, i, j, currIslandArea):
        if 0 <= i < len(lands) and 0 <= j < len(lands[0]) and lands[i][j] == '1':
            lands[i][j] = '#'
            currIslandArea[-1] += 1
            for k in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                sink(lands, k[0], k[1], currIslandArea)
    allIslandsArea = []
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[i])):
            if matrix[i][j] == '1':
                currIslandArea = [0]
                sink(matrix, i, j, currIslandArea)
                allIslandsArea.append(currIslandArea)
    return allIslandsArea


def islandsPerimeter(matrix):
    def sideContribution(matrix, i, j):
        # check the contribution this moveToCell can make, by number of '0' surrounded it
        if matrix[i][j] == '0':
            return 0
        contribution = 0
        firstLastR, firstLastC = [0, len(matrix) - 1], [0, len(matrix[0]) - 1]
        if i in firstLastR and j in firstLastC:
            # 四个角，top left, top right, bottom left, bottom right 每个都奉献2
            contribution = 2
        elif i in firstLastR or j in firstLastC:
            # the 1st or last row, or the 1st or last column 只在一条edge上边
            contribution = 1
        for k1, k2 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
            if 0 <= k1 < len(matrix) and 0 <= k2 < len(matrix[i]) and matrix[k1][k2] == '0':
                contribution += 1
        return contribution

    def sink(lands, i, j, currIslandPer):
        if 0 <= i < len(lands) and 0 <= j < len(lands[i]) and lands[i][j] == '1':
            lands[i][j] = '#'
            currIslandPer[-1] += sideContribution(lands, i, j)
            for k1, k2 in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
                sink(lands, k1, k2, currIslandPer)
    allIslandsPer = []
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[i])):
            if matrix[i][j] == '1':
                currIslandPer = [0]
                sink(matrix, i, j, currIslandPer)
                allIslandsPer.append(currIslandPer)
    return allIslandsPer


def testArea():
    inputS = ["11110,11010,11000,00000", "11000,11000,00100,00011",]
    for s in inputS:
        matrix = []
        for line in s.split(','):
            if not line:
                continue
            matrix.append([])
            for element in line:
                if element in '10':
                    matrix[-1].append(element)
        print matrix
        # print islandsArea(matrix[:])
        print islandsPerimeter(matrix)

testArea()