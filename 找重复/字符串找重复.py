# -*- coding: utf-8 -*-


# Given a string, find the first non-repeating character in it and return it's X. If it doesn't exist, return -1.
def first_unique_char(s):
    # https://leetcode.com/problems/first-unique-character-in-a-string/description/
    # 扫两次，用hash map记录词频和index
    d = {}
    for i in xrange(len(s)):
        d[s[i]] = len(s) if s[i] in d else i
    first = len(s)
    for k in d:
        first = min(first, d[k])
    return first if first < len(s) else -1


def longest_substring_without_repeating_chars(s):
    """
    https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
    用一个hash map记录，当前最长无重复字符子串的每一个字符，所对应的index
    每次遍历i位置的字符c，根据hash map判断字符c是否重复，如果是，找到上一次出现在之前的无重复子串的位置k
    那么新的以i为结尾的无重复字符子串就是k+1到i位置的子串，此时判断是否需要更新最长的长度
    需要2 pointers: start是当前无重复子串的开始index，i是当前遍历index
    """
    max_len = start = 0
    char_index = {}  # history letter index
    for i, c in enumerate(s):
        # if c in char_index and char_index[c] >= start:
        if char_index.get(c, -1) >= start:
            # 如果c是重复字符，且c的index比start要大，说明当前以i为结尾的无重复字符子串
            # 真实的开始index要比start要靠后，所以需要更新start为c的位置+1
            start = char_index[c] + 1
        else:
            # 否则，以start为开始，当前i为结尾的子串，依旧是一个无重复字符子串，判断是否要更新结果
            max_len = max(max_len, i - start + 1)
        # 无论如何，更新c的index为i
        char_index[c] = i
    return max_len

test_list = ["abba", "abcd", "abcdefg", "aaaa", "aaaab", "abcabcbb"]
for test in test_list:
    print longest_substring_without_repeating_chars(test)


def longest_substring_with_at_most_2_repeating_chars(s):
    pass