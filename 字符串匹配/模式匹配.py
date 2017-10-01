# -*- coding: utf-8 -*-


def isomorphic_strings(s, t):
    """
    https://leetcode.com/problems/isomorphic-strings/description/
    两个字符串的字符pattern是否一致，也就是每个字符对应的位置应该一致
    egg = add, foo != bar, paper = title，用hash table检查match
    """
    if len(s) != len(t):
        return False
    # 两个hash map，分别记录s->t and t->s
    ds, dt = {}, {}
    for i, c in enumerate(s):
        # 如果不存在映射 c -> t[i]，加进去，如果已经存在了，检查是否个当前t[i]相等
        if c not in ds:
            ds[c] = t[i]
        elif ds[c] != t[i]:
            return False
        if t[i] not in dt:
            dt[t[i]] = c
        elif dt[t[i]] != c:
            return False
    return True


def word_pattern(pattern, words):
    """
    https://leetcode.com/problems/word-pattern/description/
    判断s和pattern是否匹配，pattern都是单个的字母，空格分隔的words
    用一个hash map记录pattern里面的char->words里面的word的映射，以及一个hash set记录那些已经被映射的word
    遍历所有的char word pair，检查同一个char有没有map到同一个word
    其实本质上就是映射和逆映射的关系，时间空间O(N)
    """
    words = words.split()
    if len(words) != len(pattern):
        return False
    d = {}
    mapped_words = set([])  # all mapped_words of d
    for i in xrange(len(words)):
        c = pattern[i]
        w = words[i]
        # c not mapped to the same word in d
        if c in d and d[c] != w:
            return False
        # c not in d, but w already mapped by another
        elif c not in d and w in mapped_words:
            return False
        # first time see c and w, add to d and mapped_words
        else:
            d[c] = w
            mapped_words.add(w)
    return True


def word_pattern_no_delimiter(pattern, words):
    """
    https://leetcode.com/problems/word-pattern-ii/description/
    如果words里面没有分隔符，如何判断是否匹配？
    """
    if len(words) < len(pattern):
        return False

