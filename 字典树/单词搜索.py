# -*- coding: utf-8 -*-

# https://leetcode.com/problems/design-search-autocomplete-system/description/

class SentenceNode(object):
    def __init__(self, sentence, frequency):
        self.frequency = frequency
        words = sentence.split()
        self.word = words[0]
        self.is_sentence_end = False
