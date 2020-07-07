# -*- coding: utf-8 -*-

# Card game
#
# You will be building a program to play a card game. The objective of the game is to form a hand of
# three cards that for each of three different properties are either all the same or all different.
#
# The properties of a card are:
#
# 1. Prefix: +, -, or =
# 2. Letter:  A ,  B , or  C
# 3. Number of letters: 1, 2, or 3 (eg A, AA, AAA)
#
# For example, given the following set of cards
# -A -B -BB +C -C -CC =CCC
# there are two possible hands:
#
# +C -CC =CCC
# 1. Prefix: + , -, = | All different
# 2. Letter: C, C, C | All same
# 3. Number of letters: 1, 2, 3 | All different
#
# -A -B -C
# 1. Prefix: -, -, - | All same
# 2. Letter: A, B, C | All different
# 3. Number of letters: 1, 1, 1 | All same
#
# Specifications
# – You only need to find one hand
# – The cards should be read from STDIN, each card is separated by a space
# – Print the hand you find to STDOUT, space separated (trailing space is ok)
# – Cards may appear in any order in the input
# – Cards may be output in any order
# – Use the "Run Tests" button to check your solution as often as you like


class Card(object):
    def __init__(self, prefix, letter, number):
        self.prefix, self.letter, self.number = prefix, letter, number

    @staticmethod
    def allSameOrDifferentPrefix(a, b, c):
        prefixSet = {a.prefix, b.prefix, c.prefix}
        return len(prefixSet) == 3 or len(prefixSet) == 1

    @staticmethod
    def allSameOrDifferentLetter(a, b, c):
        letterSet = {a.letter, b.letter, c.letter}
        return len(letterSet) == 3 or len(letterSet) == 1


    @staticmethod
    def allSameOrDifferentNumber(a, b, c):
        numSet = {a.number, b.number, c.number}
        return len(numSet) == 3 or len(numSet) == 1


def subset_bfs(nums):
    res = [[]]
    for num in nums:
        size = len(res)
        for i in xrange(size):
            new = list(res[i])
            new.append(num)
            res.append(new)
    return res

print subset_bfs([1,2,2])
