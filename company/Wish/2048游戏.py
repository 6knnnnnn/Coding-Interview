# -*- coding: utf-8 -*-
from random import randint
from collections import defaultdict


class ValueCell(object):
    def __init__(self, x, y, val=0):
        self.x, self.y, self.val = x, y, val
        self.key = ValueCell.getKey(self.x, self.y)

    def __repr__(self):
        return "{} {} = {}".format(self.x, self.y, self.val)

    @staticmethod
    def getKey(x, y):
        return "{}:{}".format(x, y)


class GameLogic(object):
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.valueCount = defaultdict(int)
        self.availableCells = dict([])
        self.occupiedCells = dict([])
        for i in xrange(m):
            for j in xrange(n):
                cell = ValueCell(i, j)
                self.availableCells[cell.key] = cell

    def pickStartCell(self):
        if self.isBoardFull():
            return None
        # first find all candidates
        candidates = []
        for cell in self.availableCells.values():
            if self.canCellMove(cell):
                candidates.append(cell)
        if not candidates:
            return None
        # randomly pick a moveToCell
        rnd_index = randint(0, len(candidates))
        rndCell = candidates[rnd_index]
        if self.canCellMove(rndCell):
            self.occupiedCells[rndCell.key] = rndCell
            self.availableCells.pop(rndCell.key)
        rndCell.val = 2
        return rndCell

    def isBoardFull(self):
        return len(self.availableCells) == 0

    def has2048(self):
        return self.valueCount.get(2048) > 0

    def canCellMove(self, vc):
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.canCellMoveDirection(vc, i, j):
                return True
        return False

    def canCellMoveDirection(self, vc, i, j):
        x, y = vc.x + i, vc.y + j
        if 0 <= x < self.m and 0 <= y < self.n:
            key = ValueCell.getKey(x, y)
            # either empty adj moveToCell or same value that can be merged
            return key not in self.occupiedCells or self.occupiedCells[key].val == vc.val
        return False

    def getCell(self, x, y):
        key = ValueCell.getKey(x, y)
        return self.availableCells[key] or self.occupiedCells[key]

    def mergeCell(self, c1, c2):
        # merge c1 into c2, assuming they are both in occupied cells
        # update value count
        mergedVal = c1.val + c2.val
        self.valueCount[c1.val] -= 1
        self.valueCount[c2.val] -= 1
        self.valueCount[mergedVal] += 1
        # merge c2
        self.occupiedCells[c2.key].val = mergedVal
        # process c1
        self.occupiedCells.pop(c1.key)
        self.availableCells[c1.key] = c1
        c1.val = 0

    def __repr__(self):
        matrix = [[0] * self.n] * self.m
        for cell in self.occupiedCells.values():
            matrix[cell.x][cell.y] = cell.val
        for cell in self.availableCells.values():
            matrix[cell.x][cell.y] = cell.val
        return matrix


moveList = [[1, 1], [0, 1]]
game = GameLogic(4, 4)
moveIndex = 0
while not game.isBoardFull() or not game.has2048() and moveIndex < len(moveList):
    starter = game.pickStartCell()
    if not starter:
        print "cannot pick a starter moveToCell, game over"
        break
    print "pick starter:", starter.x, starter.y
    move, moveIndex = moveList[moveIndex], moveIndex + 1
    x, y = starter.x + move[0], starter.y + move[1]
    moveToCell = game.getCell(x, y)
    if not game.canCellMoveDirection(moveToCell, x, y):
        print "cannot move to {}, {}; next round".format(x, y)
        continue
    print "move {} to {}".format(starter, moveToCell)
    game.mergeCell(starter, moveToCell)
    print "new board:"
    print game.__repr__(), "\n--------"
