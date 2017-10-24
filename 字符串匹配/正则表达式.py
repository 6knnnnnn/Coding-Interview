# -*- coding: utf-8 -*-

"""
这两道题目的区别就是
1. Regex：'.*'或者'a*'，分别可以匹配0个或者多个'.'或者'a'字符，即preceding element
2. Wildcard：'?'和'*'可以是分开的，'?'代表可以match任何一个字符，'*'表示可以match一个序列的字符（包括空字符）
"""


def regular_expression_matching_recursion(regex, word):
    """
    https://leetcode.com/problems/regular-expression-matching/description/
    '.' Matches any single character.
    '*' Matches zero or more of the preceding element.
    这里面假设regex是合法的，即不存在*前边为空，或者是重复的*的情况。
    不存在*很简单，判断同一位置的每一个letter是否一致，如果不是'.'而且letter不一样，返回False
    存在 *，需要分很多种情况：
    1）'.*'，如果s的后边里面有regex里没有的字符，'.*'是可以match的，比如 s = abcde regex = .*de
        但如果regex后边有s没有的字符，不一定能match，比如 'abcde' 不可以match '.*fde' 但是'.*f*de' 可以match，但情况很复杂
    2）'a*'，需要枚举出来所有连续a的情况，直到s中连续a中断，比如 s = 'aaabc' regex = 'a*bc' 'a*abc' 'a*aabc' 'a*aaabc' 都可以
        但如果regex = 'a*aaaabc' 就不成，"越界"了，所以需要判断直到连续a终止的时候
    暴力方法，最差情况O(N!)级别，即'.*.*.*'这种情况，因为需要top-bottom，自顶向下寻找，会有很多重复的计算
    """
    def match(regex, word, ei=0, wi=0):
        # 从第一个开始判断 regex 和 word是否match
        if len(regex) == 0:
            # regex已经结束，判断word是否结束
            return len(word) == 0
        if len(regex) == 1:
            # 到达regex最后一个item了
            if regex[0][-1] != '*':
                if len(word) == 0 or regex[0] != word[0] and regex[0] != '.':
                    return False
                # 此时regex的唯一一个字母和word的第一个字母match
                # word必须只有一个字母，才能和regex完全的match，如果长度>1，不match
                return len(word) == 1
            elif regex[0] != '.*':
                # regex最后为 a*，此时需要检查，word后边是否有0或多个a，而且没有别的字符
                if len(word) == 0:
                    return True
                unique_char = set(list(word))
                return len(unique_char) == 1 and regex[0] in unique_char
            # regex的最后是 '.*'，此时无论word后边是什么，都可以match上去
            return True
        # 此时regex还有多于1个item没有处理
        if regex[0][-1] == '*':
            # * 需要考虑连续的重复字母的情况，比如aaaab 和 a*ab，要考虑 ab a+ab aa+ab aaa+ab
            # a* 和 .*当做是一个情况来对待，都需要从0开始枚举，即 0 or more preceding element
            # 每次新生成一个新的regex，比如 '.*abc*' 和 'abcd' 那么就生成 'abc*' '.abc*' '..abc*' '...abcd*'
            # 即枚举0开始，直到word的最大长度为止
            new_regex = regex[1:]
            for i in xrange(len(word)+1):
                # 要走到len(word)+1，因为每次一个新的word，必须从第一个都到最后
                # i.e. word[len-1 : ] = word[-1]，但我们想要的是直到 word[len : ]
                if word[i] == regex[0][0] or regex[0][0] == '.':
                    # 继续match的条件是，word在i位置的char和regex[0][0]相等，或者regex[0][0] = '.'
                    if match(new_regex, word[i:]):
                        return True
                else:
                    break
            return False
        elif regex[0] == word[0] or regex[0] == '.':
            # 第一个不包括*，而且第一个跟word的第一个匹配
            return match(regex[1:], word[1:])
        return False

    regex2 = list([])
    k = 0
    while k < len(regex):
        # 把 'a*' '.*' parse成为一个item，也就是之后match的时候必须一起处理
        item = regex[k]
        if k < len(regex)-1 and regex[k+1] == '*':
            item += regex[k+1]
            k += 1
        regex2.append(item)
        k += 1
    return match(regex2, list(word))


def test_regex():
    test = [
        ("wor.", "word", True), ("word.", "word", False), (".ord", "word", True), (".word", "word", False)
        ,("w*", "word", False), ("wor*d", "word", True), ("word*", "word", True), (".*ord", "word", True)
        ,(".*", "word", True), ("wo.*d", "word", True), ("word.*", "word", True), ("w.*", "word", True)
        ,(".w*", "word", False), ("wo*d", "word", False), ("word*", "word", True), ("wor*d", "worrrrd", True)
        ,("wo*.d", "word", True)
    ]

    for regex, word, matched in test:
        res = regular_expression_matching_recursion(regex, word)
        if res != matched:
            print regex, word, res
            regular_expression_matching_recursion(regex, word)

test_regex()


def regular_expression_matching_dp(e, s):
    """
    e = regex, s = word
    DP二维数组，行si，列ei，DP[si][ei]表示，从尾部开始匹配s和e，到si 和 ei的位置的时候，是否能够匹配上
    对于*的情况，需要考虑DP[si][ei+2]的数值，也就是需要初始化最后一行，和最后两列，bottom up逆向推倒至dp[0][0]
    初始化略微复杂，不同的regex有不同的结果。
    """
    # The DP table and the string s and p use the same indexes i and j, but
    # table[i][j] means the match status between p[:i] and s[:j], i.e.
    # table[0][0] means the match status of two empty strings, and
    # table[1][1] means the match status of p[0] and s[0]. Therefore, when
    # referring to the i-th and the j-th characters of p and s for updating
    # table[i][j], we use p[i - 1] and s[j - 1].

    # Initialize the table with False. The first row is satisfied.
    table = [[False] * (len(s) + 1) for _ in xrange(len(e) + 1)]

    # Update the corner case of matching two empty strings.
    table[0][0] = True

    # Update the corner case of when s is an empty string but p is not.
    # Since each '*' can eliminate the charter before it, the table is
    # vertically updated by the one before previous.

    for i in xrange(2, len(e) + 1):
        table[i][0] = table[i - 2][0] and e[i - 1] == '*'

    for i in xrange(1, len(e) + 1):
        for j in range(1, len(s) + 1):
            if e[i - 1] != "*":
                # Update the table by referring the diagonal element.
                table[i][j] = table[i - 1][j - 1] and \
                              (e[i - 1] == s[j - 1] or e[i - 1] == '.')
            else:
                # Eliminations (referring to the vertical element)
                # Either refer to the one before previous or the previous.
                # I.e. * eliminate the previous or count the previous.
                table[i][j] = table[i - 2][j] or table[i - 1][j]

                # Propagations (referring to the horizontal element)
                # If p's previous one is equal to the current s, with
                # helps of *, the status can be propagated from the left.
                if e[i - 2] == s[j - 1] or e[i - 2] == '.':
                    table[i][j] |= table[i][j - 1]

    return table[-1][-1]


def wildcard_matching(regex, word):
    """
    https://leetcode.com/problems/wildcard-matching/description/
    '?' Matches any single character.
    '*' Matches any sequence of characters (including the empty sequence).
    也可以采用类似于regular expression 的 DP解法，但也可以用贪心算法：
        1. 普通字符，检查是否完全相同即可；或者碰到了?，没所谓，当前字符匹配
        2. 如果碰到了*，需要枚举所有可能，即从*匹配0个字符开始，判断regex后边的字符是否可以和word匹配
           此时除了遍历word和regex需要的i j外，还需要两个pointer：
                star_j：最新的遇到的*的regex得位置j，每次遇到新的*的时候才需要更新
                star_i：上次用*匹配 word的位置i，当我们没有路可走，即i和j无法继续匹配了，需要回到这个star i
                        同时，从下一个star i开始，也就是star_i + 1
    例子：此时，i 和 j不匹配，j回到star_j，i不得不会到star_i的下一个，即不得不使用star_j的*来匹配c
              star_i    i
        a   b   c   d   e       ...
        a   b   *   c   d   f   ...
              star_j        j
    """
    def pre_process(regex):
        # 首先预处理一下重复的连续*
        temp = ''
        for c in regex:
            if not temp or temp[-1] != '*' or c != '*':
                temp += c
        return temp

    regex = pre_process(regex)
    i = j = 0
    star_j = star_i = -1
    while i < len(word):
        if j < len(regex) and (word[i] == regex[j] or regex[j] == '?'):
            i, j = i + 1, j + 1
        elif j < len(regex) and regex[j] == '*':
            # 找到了*，记录*出现在regex的位置j，以及对应word的开始位置i
            star_i, star_j = i, j
            # 此时j需要继续，而i不变，即假设*代表的是长度为0的任意sequence（*先忽略，之后如果遇到不能匹配的情况，再从start_i开始）
            # 如果之后 i j 匹配了，继续更新他们，也就是贪心的假设当前*所代表的长度的sequence可以满足match
            # 如果不匹配了，再从新找到之前start_i start_j的位置，再次贪心的去寻找
            j += 1
        elif star_j != -1:
            # 此时说明：i j 不匹配，而且我们之前遇到过一个*，那么j需要回到 start j + 1，即*之后的letter
            # 同时，回到了star i，不得不用*匹配 word[star_i]，且从下一个star i再次开始贪心匹配，所以每次都要更新star_i+1，以及i
            j = star_j + 1
            star_i += 1
            i = star_i
        else:
            # 此时说明没有遇见过*，那么找不到可以用来wild card的元素了，结果只能是False
            return False
    if j < len(regex) and regex[j] == '*':
        # 如果处理到word的最后，但是regex还有没处理的部分，而且regex[j] = '*'，需要挪动j+1，也就是这个*忽略了
        j += 1
    # 如果j到了regex最后，说明regex处理完了；否则regex还有内容，即j还没有到len(regex)，返回False
    return j == len(regex)
