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
    pass
