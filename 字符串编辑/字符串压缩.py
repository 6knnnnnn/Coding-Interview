# -*- coding: utf-8 -*-


def char_compression(s):
    """
    aaabbbcccaab -> a3b3c3a2b1
    Edge case：如果压缩完了长度比原始的字符串还要长，或者长度不变，就没必要压缩，比如
    Abc -> a1b1c1，aabbcc -> a2b2c2
    """
    res = list([])
    i = 0
    while i < len(s):
        j = i + 1
        count = 1
        while j < len(s) and s[j] == s[i]:
            count += 1
            j += 1
        res.append("%s%s" % (s[i], count))
        i = j
    compress = "".join(res)
    return compress if len(compress) < len(s) else s


def test():
    samples = ["aaabbbcccaab", "abc", "aabbcc", "abcc", "abccc"]
    for s in samples:
        res = char_compression(s)
        print s, res, s == res

