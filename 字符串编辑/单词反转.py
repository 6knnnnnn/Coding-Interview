# -*- coding: utf-8 -*-


# Given an input string, reverse the string word by word.
# For example, given s = "the sky is blue", return "blue is sky the".

def reverse_space_n(s):
    # https://leetcode.com/problems/reverse-words-in-a-string/description/
    # O(N)空间解很简单，输入是string类型，无论如何都要输出一个O(N)的结果
    word_list = s.split()
    i, j = 0, len(word_list)-1
    while i < j:
        word_list[i], word_list[j] = word_list[j], word_list[i]
        i, j = i+1, j-1
    return " ".join(word_list)


def reverse_space_1(char_list):
    # The input is a list of strings with length = 1
    # https://leetcode.com/problems/reverse-words-in-a-string-ii/description/
    # 如果输入是一个list of char，如何做到O(1)空间？首先把整个list反转，然后反转每一个单词，也就是遇到空格前的部分全部反转
    i, j = 0, len(char_list) - 1
    while i < j:
        char_list[i], char_list[j] = char_list[j], char_list[i]
        i, j = i + 1, j - 1
    i, j = 0, len(char_list) - 1
    while i < j:
        k = i
        while char_list[i] != ' ':
            i += 1
        # swap(s, k, i-1) # 从k到i-1位置，依次swap
        i += 1
    # 不用return，因为change in place


def reverse_word_only(s):
    # Reverse characters in a word while maintain the word’s order
    # https://leetcode.com/problems/reverse-words-in-a-string-iii/description/
    # "Let's take LeetCode contest" -> "s'teL ekat edoCteeL tsetnoc"
    # 同样也是O(N)解法，除非输入是一个char list
    L = s.split()
    output = list([])
    for w in L:
        if w: output.append(w[::-1])
    return ' '.join(output)