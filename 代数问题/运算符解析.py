# -*- coding: utf-8 -*-


def evaluate_reverse_polish_notation(tokens):
    """
    https://leetcode.com/problems/evaluate-reverse-polish-notation/description/
    ["2", "1", "+", "3", "*"] -> ((2 + 1) * 3) -> 9
    ["4", "13", "5", "/", "+"] -> (4 + (13 / 5)) -> 6
    这里面运算符没有优先级
    """
    stack = list([])
    for t in tokens:
        if t in "+-*/":
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)  # default +
            if t == '-':
                stack[-1] = b - a
            elif t == '*':
                stack[-1] = a * b
            elif t == "/":
                # here take care of the case e.g. 1/-22,
                # Python 2 returns -1, but should 0
                if a * b < 0 and b % a != 0:
                    stack[-1] = b / a + 1
                else:
                    stack[-1] = b / a
        else:
            stack.append(int(t))
    return stack.pop()
