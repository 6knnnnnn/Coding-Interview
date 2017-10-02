# -*- coding: utf-8 -*-
# 1 -> A，2 -> B，3 -> C ... 26 -> Z，27 -> AA，28 -> AB

"""
https://leetcode.com/problems/decode-ways/description/
'A' -> 1 'B' -> 2 ... 'Z' -> 26，12 可以被decode为 AB，或者 L

DP[X] 表示从后往前遍历数字到x位置，所拥有的最多的变换decode方式，肯定依赖于DP[X-1]，有可能也依赖于DP[X-2]
最小为0，最后一个为1，即只有一种方式，其他均为0
如果在x位置有2个连续0的非法情况
那么之后的dp[0..x]均为0，最后也返回0
对于DP[X]，如num[x]为0，忽略到下一个x（如果有两个连续的0，之后的
所有DP[0...x]均为0）。否则，除了DP[X+1]以外，还要看x 与x-1是否能够
组成两位数，即[1, 26] 之间，是的话，再次加上DP[X+2]
"""


def decode_ways(s):
    """
    字符串长度n，遍历的时候i理论上从n-1开始，如果s[i]不为0，初始值dp[n-1]=1，代表最后一位只有一种变换方式
    但这里dp长度为n+1，为了处理越界的情况：
        即i=n-2的时候，n-2与n-1可以两个字符组成合法数字<=26，此时需要看n的值
        所以如果dp长度为n，i=n-2的时候，i+2为n，然而dp[n]越界
        所以dp长度n+1，且dp[n]的值是1，这个dp[n]只有一种情况下会被访问
        就是当n-2与n-1能够组成两位长度的digit（<=26），我们才有dp[n-2]=dp[n-1]+dp[n]
        也就是i=n-2那么dp[i]=dp[i+1]+dp[i+2]，i+2=n；所以必须是1，代表有1中合法情况需要加到dp[i=n-2]中
    反之dp长度为n，需要单独处理越界的情况
    """
    if not s: return 0
    if len(s) == 1:
        return 1
    dp = [0] * (len(s)+1)
    dp[-1] = 1
    if s[-1] != '0':
        dp[-2] = 1
    for i in xrange(len(s)-2, -1, -1):
        if s[i] != '0': # 不是0才考虑当前i，否则看下一个i
            dp[i] = dp[i+1]
            if int(s[i:i+2]) <= 26:
                dp[i] += dp[i+2]
    return dp[0]


def decode_ways_2_variables(s):
    if not s or s[0] == '0': return 0
    if len(s) == 1:
        return 1
    dp2 = dp1 = 1 # 初始均为1
    for i in xrange(1, len(s)):
        if s[i] == '0':
            dp1 = 0 # 如果在x位置有2个连续0的非法情况，那么之后的dp1 dp2 均为0，最后也返回0
        if s[i - 1] == '1' or (s[i - 1] == '2' and s[i] not in '789'):
            # 有两位的情况：1x必定合法，但是2x中x必须<=6
            dp2, dp1 = dp1, dp1 + dp2 # 滚动更新
        else:
            dp2 = dp1 # 如果只能组成2-9之间的单一数字
    return dp1


def excel_sheet_column_title(n):
    """
    https://leetcode.com/problems/excel-sheet-column-title/description/
    给定一个数，返回对应的excel表格列名
    n 拆分成两个部分，n/26 * ? + n % 26
    ABCD＝A×26³＋B×26²＋C×26¹＋D＝1×26³＋2×26²＋3×26¹＋4 = 19010
    ZZZZ＝Z×26³＋Z×26²＋Z×26¹＋Z＝26×26³＋26×26²＋26×26¹＋26 = 475254
    """
    cols = ""
    while n:
        # 逆序，先生成最小的title，加入到结果中去，然后找次小的
        # (n-1)%26 是因为我们想到得到的是[0, 25]
        x = (n - 1) % 26
        # 'A' = 65, 把x转化为ASCII
        cols = chr(x + 65) + cols
        # 更新n
        n = (n - 1) / 26
    return cols


def excel_sheet_column_number(column):
    """
    https://leetcode.com/problems/excel-sheet-column-number/description/
    Base 26, BCA = 2*26^2 + 3*26^1 + 1*26^0
    """
    number, length = 0, len(column)-1
    for c in column:
        digit = ord(c) - 64
        number += digit * (26**length)
        length -= 1
    return number


for _ in [26, 27, 28, 1431]:
    print _, excel_sheet_column_title(_)

