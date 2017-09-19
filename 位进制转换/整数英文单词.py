# -*- coding: utf-8 -*-


def integer_to_english_words(num):
    """
    https://leetcode.com/problems/integer-to-english-words/description/
    给定一个非负数字，返回他的英文单词表达。
    123 -> "One Hundred Twenty Three"
    12,345 -> "Twelve Thousand Three Hundred Forty Five"
    1,234,567 -> "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
    """
    _1_to_19 = "One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve " \
               "Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen".split()
    _20_to_90 = "Twenty Thirty Forty Fifty Sixty Seventy Eighty Ninety".split()

    def dfs(n):
        # 返回的是一个list，对应的是英文单词
        if n < 20:
            return _1_to_19[n-1:n]
        if n < 100:
            # 此时 20<=n<100，比如34，那么34/10-2=1 即Thirty，34%10=4，即Four
            _20_to_90_val = _20_to_90[n/10-2]
            return [_20_to_90_val] + dfs(n % 10)
        if n < 1000:
            # 此时 100<= n<1000，比如678，那么，百位就是6，即Six Hundreds，十位是68，递归调用DFS
            _100_ = _1_to_19[n / 100 - 1]
            return [_100_, 'Hundred'] + dfs(n % 100)
        # 此刻说明 n >= 1000，那么需要找到它最大位，即找到 Thousand, Million 还是 Billion
        if len(str(n)) <= 6:
            # 12,345      即 3<=长度<=6， 拆分为 [12] [Thousand] [345]
            return dfs(n / 1000) + ['Thousand'] + dfs(n % 1000)
        elif len(str(n)) <= 9:
            # 123,456     即 6<=长度<=9， 拆分为 [1] [Million] [23,456]
            return dfs(n / 1000000) + ['Million'] + dfs(n % 1000000)
        elif len(str(n)) <= 12:
            # 123,456,789 即 9<=长度<=12，拆分为 [1] [Billion] [23,456,789]
            return dfs(n / 1000000000) + ['Billion'] + dfs(n % 1000000000)
    res = dfs(num)
    return ' '.join(res) if num != 0 else 'Zero'

for n in [1234567890, 123, 12345, 0, 12, 21]:
    print n, integer_to_english_words(n)
