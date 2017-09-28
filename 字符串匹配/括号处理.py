# -*- coding: utf-8 -*-


def valid_parentheses(s):
    """
    https://leetcode.com/problems/valid-parentheses/description/
    只包含'(', ')', '{', '}', '[' and ']'，检查是否合法，map+stack
    """
    stack = list([])
    valid_map = {"(": ")", "{": "}","[": "]"}
    for c in s:
        if c in valid_map:
            stack.append(c)
        elif not stack or valid_map[stack.pop()] != c:
            return False
    return len(stack) == 0


def generate_parentheses(n):
    """
    https://leetcode.com/problems/generate-parentheses/description/
    给定n，返回n对括号的所有排列组合数目，比如n=3，所有可能为："((()))", "(()())", "(())()", "()(())", "()()()"
    回溯法DFS，类似于组合，每次DFS，根据剩余的left 和 right 括号的数量，以及当前的括号string，来判断是否需要向左以及向右走
    先是去left，当right比left大的时候，再去right；当right括号为0的时候，说明当前的括号string满足条件了，加入到结果中去
    """
    def dfs(curr_p, left, right, results):
        if not right:  # end this sequence
            results.append(curr_p)
            return
        if left:
            dfs(curr_p + '(', left - 1, right, results)
        if right > left:
            dfs(curr_p + ')', left, right - 1, results)

    results = []
    dfs('', n, n, results)
    return results


def remove_invalid_parenthesis():
    pass
