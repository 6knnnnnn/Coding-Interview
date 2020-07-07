from collections import defaultdict
from heapq import *


class TrieNode(object):
    def __init__(self):
        self.children = dict()
        self.sentences = set()

    def __repr__(self):
        if self.sentences:
            return "{} - {}".format(list(self.sentences)[0], self.sentences)
        return "None"


class SentenceFrequency(object):
    def __init__(self, sentence, frequency):
        self.sentence, self.freq = sentence, frequency

    def __lt__(self, other):
        if self.freq == other.freq:
            return self.sentence < other.sentence
        return self.freq < other.freq

    def __repr__(self):
        return "{} - {}".format(self.sentence, self.freq)


class AutoCompleteSystem(object):
    def __init__(self, sentences, counts):
        self.currentS = ''
        self.topK = 3
        self.sentences = defaultdict(int)
        self.currentTrieNode = self.trieRoot = TrieNode()
        for i, s in enumerate(sentences):
            self.sentences[s] = SentenceFrequency(s, counts[i])
            self.addSentence(s)

    def addSentence(self, sentence):
        node = self.trieRoot
        for c in sentence:
            if c not in node.children:
                node.children[c] = TrieNode()
            node.sentences.add(sentence)
            node = node.children[c]

    def input(self, c):
        if c == "#":
            # reset the current sentence
            self.sentences[self.currentS].freq += 1
            self.addSentence(self.currentS)
            self.currentS = ''
            self.currentTrieNode = self.trieRoot
        else:
            self.currentS += c
            if self.currentTrieNode:
                self.currentTrieNode = self.currentTrieNode.children.get(c)
                # find the top k sentences
                pq = []
                for sentence in self.currentTrieNode.sentences:
                    sentenceFreq = self.sentences[sentence]
                    if len(pq) == self.topK:
                        heappushpop(pq, sentenceFreq)
                    else:
                        heappush(pq, sentenceFreq)
                return pq
        return []


def test1():
    sentences, counts = ["i love you", "island", "ironman", "i love leetcode"], [5,3,2,2]
    acs = AutoCompleteSystem(sentences, counts)
    inputs = [
        "i love you#", "island#", "i love leetcode#",
    ]
    for word in inputs:
        for c in word:
            print c, acs.input(c)

test1()

