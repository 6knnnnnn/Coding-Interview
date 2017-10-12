# -*- coding: utf-8 -*-


def evaluate_reverse_polish_notation(tokens):
    """
    https://leetcode.com/problems/evaluate-reverse-polish-notation/description/
    ["2", "1", "+", "3", "*"] -> ((2 + 1) * 3) -> 9
    ["4", "13", "5", "/", "+"] -> (4 + (13 / 5)) -> 6
    这里面运算符没有优先级
    Follow up可能是，如果有优先级，即 * = / > + = -，甚至是引入幂运算？
    1 + 2 * 3 + 4，要先扫一遍，把高级运算符当做是nested list，放到stack中
    之后扫stack，每次都先计算出每个stack top value，之后再继续
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
