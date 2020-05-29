# -*- coding: utf-8 -*-


def word_search(board, word):
    """
    https://leetcode.com/problems/word-search/description/
    根据一个matrix，里面有letter，判断是否可以通过相邻cell来组成目标word，不能有cell的复用
    有点类似于数岛屿的问题，可以把cell sink掉，也就是换成别的value，之后遍历结束，在recover
    比如："ABCCED" -> True, SEE -> True, ABCB -> False
    ['A','B','C','E'],
    ['S','F','C','S'],
    ['A','D','E','E']
    空间O(W)，即word的长度（递归调用最多W次）；时间O(M * N * W * 4)，每个字母都要遍历四个方向
    可能的edge case：如果word的长度W > M*N，那就不需要找了
    Follow up: 如果8个方向呢？即对角线也成立？改变for循环的条件，
    """
    def dfs(b, x, y, word, word_index):
        # 判断坐标(x, y)是否等于word在word_index位置的letter，如果是，继续下一层搜索
        if word_index >= len(word):
            # 如果到头了，说明找到了一个匹配的走法，返回True
            # 如果需要记录path，多两个变量，分别为current and global_list，此时把curr加到global里面
            return True
        found = False
        if 0 <= x < len(b) and 0 <= y < len(b[0]):
            if b[x][y] == word[word_index]:
                copy, b[x][y], word_index = b[x][y], "#", word_index + 1
                for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if found:
                        break
                    found = dfs(b, i, j, word, word_index)
                b[x][y] = copy  # reset back to original
        return found

    for x in xrange(len(board)):
        for y in xrange(len(board[0])):
            if dfs(board, x, y, word, 0):
                return True
    return False


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
    https://leetcode.com/problems/word-search-ii/description/
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


def get_adj(x, y, diagonal=False):
    # 给定矩阵中的一个x和y坐标，返回相邻cell的坐标（无论是否越界），如果对角线为True，返回8个方向的坐标
    res = list([])
    if diagonal:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == j == 0:
                    continue
                res.append((x+i, y+j))
    else:
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            res.append((x + i, y + j))
    return res
