# -*- coding: utf-8 -*-
from collections import defaultdict


def is_palindrome(word):
    l, r = 0, len(word)-1
    while l <= r:
        if word[l] != word[r]:
            return False
        l, r = l + 1, r - 1
    return True


def palindrome_pairs(words):
    """
    给定一组word 数组，找到里面所有可能的两两组合为一个palindrome pairs，返回pair index，要讲究顺序
    sentences = ["abcd", "dcba", "lls", "s", "sssll"]，返回的是index：[[0, 1], [1, 0], [3, 2], [2, 4]]
    即The palindromes are ["dcbaabcd", "abcddcba", "slls", "llssssll"]
    暴力解法：对于所有可能的pair，判断是否为回文，所有的pair数量为N^N，假设每个word的平均长度为M，那么一个pair就是2M
    之后再检查是否是回文M时间，所以总的时间复杂度为O(M*N^2)

    优化解法：其实对于任意一个word，我们可以把它任意的分为左右两部分，即left | right
    如果其中有一个部分已经是回文了，说明对于另一个部分，我们需要找到它的翻转单词，这样子这两个单词和到一起之后，就是一个回文pair了
    那么对于可能的candidate只有情况：
    1）left  是 palindrome，那么可能的组合是 candidate | left | right，candidate就是right的翻转
    2）right 是 palindrome，那么可能的组合是 left | right | candidate，而这里candidate是left的翻转
    所以，一开始有个hashmap = reverse word->index map，把翻转的字符串的index保存下来，这样在后面切字符串的时候，方便查询
    需要有两层for循环来解决，因为要找到所有可能的分割+翻转组合，以及最后可能有重复的结果
    """
    index_map = dict([])
    # 假设没有重复的单词，重复的话value=list，那么之后求出所有组合即可
    for i, word in enumerate(words):
        # 需要reverse word
        index_map[word[::-1]] = i
    # 记录的是，对于某个index as key，value是可以和它组合成palindrome的word index set，即set用来取重复
    res_map = defaultdict(set)
    for i, word in enumerate(words):
        # 三种切法，最左边，中间，最右边，所以j的长度就是到len(word)
        for j in xrange(len(word)+1):
            left, right = word[:j], word[j:]
            if is_palindrome(left) and right in index_map and index_map[right] != i:
                # 这里面顺序正过来的，也就是 candidate | left | right，candidate在当前word的左边
                res_map[index_map[right]].add(i)
            if is_palindrome(right) and left in index_map and index_map[left] != i:
                # 这里面顺序反过来的，也就是 left | right | candidate，candidate在当前word的右边
                res_map[i].add(index_map[left])
    res_list = []
    for k, v in res_map.items():
        for index in v:
            res_list.append([k, index])
    return res_list

a = ["abcd","dcba","lls","s","sssll"]

print palindrome_pairs(a)
