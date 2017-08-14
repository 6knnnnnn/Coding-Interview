# -*- coding: utf-8 -*-

# 名人不认识任何人，所有人都认识名人
# 如果x knows y，x肯定不是名人，如果x doesn't know y，y肯定不是名人，所以依次排除


def knows(x, y):
    return False


def findCelebrity(n):
    if n < 0: return 0
    x, y = 0, n - 1
    # two pointers，前后扫
    while x < y:
        if knows(x, y):
            x += 1
        else:
            y -= 1
    for i in xrange(n):
        if i != x and (knows(x, i) or not knows(i, x)):
            # 如果存在x认识任何人或者任何人不认识x，不存在名人
            return -1
    return x