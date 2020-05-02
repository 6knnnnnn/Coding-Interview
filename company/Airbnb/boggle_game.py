# -*- coding: utf-8 -*-
"""
类似于word search ii，但是不同的是，每个单词只能用一次
所以这里面需要找到的是，最后能够根据词典和board里面的单词，match的最多的数量

"""


class TrieNode(object):
    def __init__(self):
        # 这里面并没有用is word flag瀬判断是否是word，而是直接用word是否为None
        self.word = None
        self.children = {}


class Trie(object):
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.word = word


def word_search_multiple_words(board, words):
    """
    对于多个word，同样的要求，如果用同样的方法，遍历所有cell，假设有K个word，那么总的时间复杂度为O(M N W K)
    可以用Trie优化，根据word list建立一个Trie，时间+空间复杂度 O(W * K)，假设每个word平均长度为W
    然后search用同样的方式，从某个cell开始，判断Trie里面是否有对应的letter，如果有就继续
    所以就相当于，仍旧是遍历一遍board，但是每次遍历到某个cell的时候，根据Trie来判断是否需要继续，而不是遍历了每个word来判断
    所以，如果单词之间的overlap比较多，比如ABC ABD ABE... 可以很好地节省时间，因为之前搜过得就不用重复在搜了
    """
    def dfs(board, i, j, root, exist_words):
        # 所以此时DFS不再需要word 和 start两个参数了，相当于把所有word放到了一个字典里
        # 如果是原来的方法，每次还要记录对应的word和对应的start，会有很多重复工作
        if 0 <= i < len(board) and 0 <= j < len(board[0]):
            letter = board[i][j]
            if letter and letter in root.children:
                board[i][j], root = None, root.children[letter]
                if root.word:
                    # 找到了一个word，即word不为None，此时需要把word变为None，以避免重复
                    # 比如从 ["aa"] 里面找"a"，如果不去重复，会有["a", "a"]，或者可以用hash set
                    exist_words.add(root.word)
                    root.word = None
                for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                    dfs(board, x, y, root, exist_words)
                board[i][j] = letter # recover

    res = list([])
    if board:
        tree = Trie()
        for word in words:
            tree.insert(word)

        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                dfs(board, i, j, tree.root, res)
    return res
