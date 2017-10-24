# -*- coding: utf-8 -*-
from collections import deque


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
    大概就是类似于DFS+剪枝，每一层（长度），通过删除每一个位置的括号，来找到该层所有可能的括号组合
    如果其中有任意一个组合满足合法，就说明之后如果再次进行删除，肯定会不合法，所以此时停止DFS，返回结果
    需要注意去重复，即对于当前长度（层）的string，删除某一个位置后的结果，在之前已经"恰好"产生过了，此时重复
    """
    def is_valid(s):
        cnt = 0
        for c in s:
            cnt += 1 if c == '(' else (-1 if c == ')' else 0)
            if cnt < 0:
                # 此时说明有一个unmatched右括号，那肯定不match
                return False
        return cnt == 0

    visited = set([s]) # 用来去重复
    ans = [] # 最后的结果
    queue = deque([s]) # 需要之后继续处理的产生出来的string
    while queue and not is_valid(queue[0]):
        # queue里面，第一次找到可能的valid的结果的时候，则不再向队列中补充新的可能字符串
        # 因为如果再进一步去删除某个括号，肯定会导致不合法的出现
        curr = queue.popleft()
        for x in xrange(len(curr)):
            if curr[x] in ('(', ')'):
                # 移除每一个位置的括号，生成新的字符串加入队列中去，如果没有重复的话
                new = curr[:x] + curr[x + 1:]
                if new not in visited:
                    visited.add(new)
                    queue.append(new)
    while queue:
        # 此时，如果queue中有剩余元素，需要处理完
        curr = queue.popleft()
        if is_valid(curr):
            ans.append(curr)
    return ans
