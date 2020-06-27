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

numbers = "0123456789"
operators = "+-*/"


def basic_calculator(s):
    """
    https://leetcode.com/problems/basic-calculator/description/
    其实和下边的一个道理，只不过这里面只有加减法，以及可能会有括号
    "(1+(4+5+2)-3)+(6+8)" = 23
    """
    # pre-process input s
    i, j = 0, len(s)-1
    while i < j and s[i] != '(':
        i += 1
    while i < j and s[j] != ')':
        j -= 1
    if i < j and s[i] == '(' and s[j] == ')':
        # find a parenthesis pair
        nestedRes = basic_calculator(s[i+1:j])
        newExpression = "{}{}{}".format(s[:i], nestedRes, s[j+1:])
        return basic_calculator(newExpression)
    else:
        # no parenthesis
        numStack, operStack, i = [], [], 0
        while i < len(s):
            c = s[i]
            if c in operators:
                operStack.append(c)
                i += 1
            elif c in numbers:
                j = i
                while j < len(s) and s[j] in numbers:
                    j += 1
                num = int(s[i:j])
                numStack.append(num)
                i = j
    # now calculate values from two stacks
    while operStack and numStack:
        operator = operStack.pop()
        n1 = numStack.pop()
        n2 = numStack.pop() if numStack else 0
        if operator == '-':
            numStack.append(n2 - n1)
        elif operator == "+":
            numStack.append(n2 + n1)
    return numStack[-1]


print basic_calculator("(1+2)")
print basic_calculator("(1+2)+3")
print basic_calculator("(1+2)+(4-5)")
print basic_calculator("1+2-4")


def basic_calculator_ii(s):
    """
    https://leetcode.com/problems/basic-calculator-ii/description/

    给定一个string表达式，里面只包含有非负整数，以及加减乘除运算符，或者空格，解析表达式的最后的结果

    "3+2*2" = 7，" 3/2 " = 1，" 3+5 / 2 " = 5
    用stack模拟，这里面stack存放的都是需要做"加法"的元素，最后stack求和即可：
        即如果遇到了乘除法，把他们的结果计算出来，压缩成为一个数字，放到stack里面
        而如果只是加减法，把对应的符号加入到stack里面，下次遇到的数字跟这个符号相乘，就是最后需要"加上"的元素值
        注意正负号的处理，特别是python的负数除法
    """
    def find_number(s, start):
        # return the numbers that beginning from start index
        end = start + 1
        while end < len(s) and s[end] in numbers:
            end += 1
        num = int(s[start: end])
        # return end as the new starting index
        return num, end
    s = s.replace(" ", "")
    # 需要初始化stack为[1]，即第一位数字永远是乘以1
    stack, i = list([1]), 0
    # i用来指向运算符，j用来找数字digit
    while i < len(s):
        if s[i] in numbers:
            num, i = find_number(s, i)
            stack[-1] *= num
        elif s[i] in operators:
            if s[i] in "+-":
                # 此时加入后边元素的符号，因为我们一直都在做"加法"
                stack.append(-1 if s[i] == "-" else 1)
                i += 1
            elif s[i] in "*/":
                # 需要进行压缩，即把所有乘除法操作的component计算出来
                a = stack.pop()
                while i < len(s) and s[i] in "*/":
                    op = s[i]
                    b, i = find_number(s, i+1)
                    if op == "*":
                        a *= b
                    elif op == "/":
                        # 需要注意的是，在python里面，负数除法的特殊性，即-3/2=-2，但其实是-1
                        if a >= 0:
                            a /= b
                        else:
                            a /= -b
                            a = -a
                # 压缩完毕，加入到stack中
                stack.append(a)
    return sum(stack)


def test1():
    samples = [ "14-3/2", "1 + 1", "1 + 2 * 3", "3+2*2", "3/2", "3 + 5 / 2", "123", "1 + 1"]
    for t in samples: print basic_calculator_ii(t)
