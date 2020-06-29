# -*- coding: utf-8 -*-

"""
https://www.1point3acres.com/bbs/forum.php?mod=viewthread&tid=580781&ctid=229044

一个数组内部有红绿两种灯，[R, G, G, R, G]，找到一个subarray，使得：当把红灯绿灯反转后，里面绿灯的数量最多
红灯 = -1，绿灯 = 1，本质就是，把所有红灯绿灯互换，然后max subarray
"""


def maxGreenLightsSwap(lights):
    dp = [0] * len(lights)
    maxVal = 0
    dp[0] = -1 if lights[0] == 'G' else 1
    for i in xrange(len(lights)):
        n = -1 if lights[i] == 'G' else 1
        dp[i] = n
        if i > 0 and dp[i-1] > 0:
            dp[i] += dp[i-1]
        maxVal = max(maxVal, dp[i])

    res = []
    i = len(dp)-1
    while i >= 0:
        if dp[i] == maxVal:
            # meet one subarray, need to find the starting index i where i == 0 but i+1 > 0
            end = i
            while i >= 0 and dp[i] > 0:
                i -= 1
            res.append((lights[i+1:end+1], [i+1, end]))
        else:
            i -= 1

    return res, dp


def maxGLightsSwap(lights):
    # O(1) space
    currSum = maxVal = start = end = 0
    for i, light in enumerate(lights):
        n = 1 if light == 'R' else -1
        if currSum <= 0:
            start = i
            currSum = n
        else:
            currSum += n
        if currSum > maxVal:
            maxVal = currSum
            end = i

    return lights[start: end+1] if maxVal > 0 else []


for lights in [
    ['R', 'G', 'G', 'G', 'R'],
    ['R', 'G', 'R', 'G', 'R', 'R', 'R', 'G', 'R', 'G', 'R', 'R', 'G'],
    ['G'] * 10,
]:
    print lights
    print maxGreenLightsSwap(lights)
    print maxGLightsSwap(lights)
    print "-------"
