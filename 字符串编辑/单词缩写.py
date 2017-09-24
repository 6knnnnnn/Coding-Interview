# -*- coding: utf-8 -*-


def valid_word_abbreviation(word, abbr):
    """
    判断一个word和一个abbr是否匹配
    非数字位置的字符是否相等，数字位置的字符所组成的长度是否相等
    https://leetcode.com/problems/valid-word-abbreviation/description/
    """
    if len(abbr) > len(word):
        return False
    i = j = 0
    # two pointers
    while i < len(word) and j < len(abbr):
        if word[i] == abbr[j]: # 合法的字母且相等，分别+1
            i, j = i+1, j+1
        elif abbr[j] in '123456789': # j为1-9的数字
            k = j+1 # 找到[j...k-1]，包含数字
            while k < len(abbr) and abbr[k] in '1234567890':
                k += 1
            i += int(abbr[j:k]) # [j...k-1]=数字，就是i下次起点
            j = k
        else:
            # j与i不相等，且j位置为0或者其它，返回False
            return False
    return i == len(word) and j == len(abbr) # 同时抵达末尾才算match


def test_valid_word_abbreviation():
    word = "word"
    abbr = ["word", "1ord", "w1rd", "wo1d", "wor1", "2rd", "w2d", "wo2", "1o1d", "1or1", "w1r1", "1o2", "2r1", "3d", "w3", "4"]
    for a in abbr:
        print word, a, valid_word_abbreviation(word, a) # All true
    print valid_word_abbreviation(word = "internationalization", abbr = "i12iz4n") # True
    print valid_word_abbreviation(word = "apple", abbr = "a2e") # False


# https://leetcode.com/problems/unique-word-abbreviation/description/
# Assume you have a dictionary and given a word, find whether its abbreviation
# is unique in the dictionary. A word's abbreviation is unique if no other word
# from the dictionary has the same abbreviation.
# Unique定义：词典中没有除了这个word以外，跟target的缩写一样的单词。
# 如果word不在单词中，或者没有别的word的缩写，也算是unique。
class ValidWordAbbr(object):
    @staticmethod
    def get_abbr(word):
        # 创建缩写，word->w2d
        if not word:
            return ""
        if len(word)< 2:
            return word
        return "{}{}{}".format(word[0], len(word)-2, word[-1])

    def __init__(self, dictionary):
        self.abbrMap = {}
        for word in dictionary:
            abbr = ValidWordAbbr.get_abbr(word)
            if abbr not in self.abbrMap:
                self.abbrMap[abbr] = set([])
            # 缩写->单词集合
            self.abbrMap[abbr].add(word)

    def isUnique(self, word):
        abbr = ValidWordAbbr.get_abbr(word)
        # 如果word的缩写没出现在词典中，或者有缩写，但是缩写对应的单词set只有这个word，就是unique
        return abbr not in self.abbrMap or (word in self.abbrMap[abbr] and len(self.abbrMap[abbr]) == 1)

    def __repr__(self):
        return str(self.abbrMap)


def test_valid_word_abbr():
    dictionary = ["deer","door","cake","card"]
    word_list = ["dear","cart","cane","make"]
    # Expected: [false,true,false,true]
    vwa = ValidWordAbbr(dictionary)
    for w in word_list:
        print w, vwa.isUnique(w)
    dictionary = ["hello", "hell", "hill"]
    word_list = ["hello", "hell", "helle"]
    # Expected: [True, False, True]
    vwa = ValidWordAbbr(dictionary)
    for w in word_list:
        print w, vwa.isUnique(w)
