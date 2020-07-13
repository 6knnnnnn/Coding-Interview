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

prefixes = "+-="
letters = "ABC"
numbers = [1,2,3]



def binarySearch(cards, start, target):
    l, r = start, len(cards) - 1
    while l <= r:
        mid = (l+r) / 2
        if cards[mid] == target:
            return True
        if cards[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    return False


def getTargetField(f1, f2, fields):
    if f1 == f2:
        return f1
    for f in fields:
        if f != f1 and f != f2:
            return f


def findTargetHand(inputs):
    results = []
    cards = inputs.split(" ")
    cards.sort()
    for i in xrange(len(cards)-2):
        for j in xrange(i+1, len(cards)-1):
            c1, c2 = cards[i], cards[j]
            p3 = getTargetField(c1[0], c2[0], prefixes)
            l3 = getTargetField(c1[1], c2[1], letters)
            n3 = getTargetField(len(c1)-1, len(c2)-1, numbers)
            target = "{}{}".format(p3, l3 * int(n3))
            if binarySearch(cards, j+1, target):
                results.append((c1, c2, target))
    return results

inputs = "-A -B +A -BBB -BB +C -C -CC +AA +BBB =BBB"
# inputs = "-A -B -BB +C -C -CC =CCC"
print findTargetHand(inputs)
