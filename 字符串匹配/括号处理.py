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


def remove_invalid_parenthesis(s):
    """
    https://leetcode.com/problems/remove-invalid-parentheses/description/
    解法：https://www.hrwhisper.me/leetcode-remove-invalid-parentheses/
    把string里面的所有非法括号删除掉，要求找到所有可能的合法括号，string里面可能有其他非括号字母比如：
    "()())()" -> ["()()()", "(())()"]，"(a)())()" -> ["(a)()()", "(a())()"]，")(" -> [""]

    """
    def is_valid(s):
        cnt = 0
        for c in s:
            if c == '(':
                cnt += 1
            elif c == ')':
                if cnt == 0:
                    return False
                cnt -= 1
        return cnt == 0

    curr_p = {s}
    while curr_p:
        # filter的作用就是，对于curr p里面的每一个元素，如果满足filter function为True，就加到结果中去，否则删除
        ans = filter(is_valid, curr_p)
        if ans:
            # 每次找到新的一层，如果此时有结果，说明找到了合法的括号，而如果再进一步去删除某个括号，肯定会导致不合法的出现
            # 所以此时只需要返回即可。
            return ans
        # 没有找到，那么找下一层
        next_p = set([])
        for cur in curr_p:
            print cur, ':-----'
            for i in xrange(len(cur)):
                # remove i from cur
                print cur[i], "->", cur[:i], "+", cur[i + 1:]
                new = cur[:i] + cur[i + 1:]
                next_p.add(new)
        # curr_p = {cur[:i] + cur[i + 1:] for cur in curr_p for i in xrange(len(cur))}
        curr_p = next_p

s1 = "()())()"
print remove_invalid_parenthesis(s1)