# -*- coding: utf-8 -*-


class TrieNode(object):
    # 字典树结构，需要注意的是，每个word的结尾时刻，需要加一个flag判断，是否是word（而非仅仅是一个path）
    def __init__(self, letter):
        self.letter = letter
        # 其实不一定需要这个letter和is word flag，而是另一种更好的实现方式
        self.is_word = False
        self.child_node_map = dict([])

    def update_word(self, is_word):
        self.is_word = is_word

    def has_child(self, c):
        return self.child_node_map.get(c) is not None


class Trie(object):
    def __init__(self):
        # root头结点为空字符
        # https://leetcode.com/problems/implement-trie-prefix-tree/description/
        self.root = TrieNode('')

    def insert(self, word):
        # 插入一个新的word到字典树，需要在最后的时候，更新TrieNode为一个word flag
        node = self.root
        for i, c in enumerate(word):
            if c not in node.child_node_map:
                node.child_node_map[c] = TrieNode(c)
            node = node.child_node_map[c]
        if node and node != self.root:
            node.update_word(True)

    def go_to_last_node(self, word):
        # 给定一个word，从root开始，根据word的每一个char，遍历到最后一个节点并返回，如果不存在，则返回None
        node = self.root
        for i, c in enumerate(word):
            node = node.child_node_map.get(c)
            if not node:
                return None
        return node if node != self.root else None

    def search(self, word):
        # 判断字典树中，word是否存在，需要走到头，然后判断TrieNode 的word flag
        last_node = self.go_to_last_node(word)
        return last_node is not None and last_node.is_word

    def start_with(self, prefix):
        # 其实就是沿着prefix，从root开始走到头，如果最后还是有节点，那么说明有path即prefix存在，不用判断是否为word
        last_node = self.go_to_last_node(prefix)
        return last_node is not None

    def search_wildcard(self, wild_card_word):
        """
        https://leetcode.com/problems/add-and-search-word-data-structure-design/
        支持search wildcard word，即'.'代表任何字符，基本跟Trie一样
        区别是每当遇到一个'.'的时候，找到当前node的所有的child node，所以此题目不需要产生26个字母以次遍历
        """
        def dfs(node, word):
            for i, c in enumerate(word):
                if c == '.':
                    for k in node.child_node_map:
                        if dfs(node.child_node_map[k], word[i+1:]):
                            # 递归调用search_wildcard
                            return True
                    return False
                elif c not in node.child_node_map:
                    return False
                node = node.child_node_map[c]
            return node.is_word
        return dfs(self.root, wild_card_word)

    def remove(self, word):
        # 删除某个word，如果这个word下边没有child，直接删除node，否则，把is word flag标记为False
        node = self.go_to_last_node(word)
        if node:
            if node.child_node_map:
                node.is_word = False
            else:
                parent = self.go_to_last_node(word[:-1])
                parent.child_node_map.pop(node.letter)
