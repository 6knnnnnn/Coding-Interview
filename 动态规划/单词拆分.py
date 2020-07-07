# -*- coding: utf-8 -*-

"""
给定一个string，和一个词典（无重复），词典里面的单词可以复用。
判断是否能够通过词典里面word组成s，举例：
"leetcode", ["leet","code"] -> True
"leetcode", ["leet","codes"] -> False
"leetcodecode", ["leet","code"] -> True

DP是一维数组，DP[i]表示，s[0:i-1]是否能够被break
所以dp[len(s)]表示s[0:len(s)-1]是否能break，dp[0]初始化为True，即如果s为空，那么肯定能break（没有可能也是一种可能）

那么，对于任意一个dp[i]，跟子问题的依赖关系为：
dp[i] = True If and only if
存在一个 0<=j<=i-1，使得s[j:i]这个sub word存在于字典中，而且，dp[j]为True，即s[0:j-1] breakable

如果任一条件不满足，dp[i]肯定为False

比如 s=leetcode，和字典[leet, code]

    l	e   e	t	c	o	d	e
0	1	2	3	4	5	6	7	8
T	F	F	F	T	F	F	F	T

Follow up: Word break II，或者每个word的使用次数有限（只能用1次？n次？）
"""


def word_break(s, word_dict):
    # https://leetcode.com/problems/word-break/description/
    word_dict = set(word_dict)
    # 默认所有dp除了dp[0]都是False
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in xrange(1, len(s) + 1):
        # 从 1 -> len(s)，因为最后要求的是dp[len(s)]
        for j in xrange(i):
            # 从 0 到 i-1，如果有任意一个j满足 dp[j]=True，而且sub word s[j:i]在字典中，dp[i]就为True
            if dp[j] and s[j:i] in word_dict:
                dp[i] = True
                break
    return dp[-1]


def word_break_all_possible_path(s, word_dict):
    """
    判断是否能够组成s的同时，找到所有可能的组合
    https://leetcode.com/problems/word-break-ii/discuss/718628/Using-Word-Break-I-solution-as-a-check-to-prune-the-solution-to-Word-Break-II
    """