# -*- coding: utf-8 -*-

# http://www.lintcode.com/zh-cn/problem/strings-serialization/

# 需要考虑 连接符，转义符的处理


def caesar_cipher(s, k):
    """
    凯撒密码 https://en.wikipedia.org/wiki/Caesar_cipher
    abc + 2 -> cde, a + 26 -> a, a + 27 -> b, xyz + 2 -> zab
    """
    res = list([])
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for c in s:
        i = (ord(c) - 97 + k) % 26
        res.append(alphabet[i])
    return "".join(res)
