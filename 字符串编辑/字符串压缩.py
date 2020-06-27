# -*- coding: utf-8 -*-


def char_compression(s):
    """
    aaabbbcccaab -> a3b3c3a2b1
    Edge case：如果压缩完了长度比原始的字符串还要长，或者长度不变，就没必要压缩，比如
    Abc -> a1b1c1，aabbcc -> a2b2c2
    """
    res = list([])
    i = 0
    while i < len(s):
        j = i + 1
        count = 1
        while j < len(s) and s[j] == s[i]:
            count += 1
            j += 1
        res.append("%s%s" % (s[i], count))
        i = j
    compress = "".join(res)
    return compress if len(compress) < len(s) else s


def test():
    samples = ["aaabbbcccaab", "abc", "aabbcc", "abcc", "abccc"]
    for s in samples:
        res = char_compression(s)
        print s, res, s == res


class CompressedStringIterator(object):
    """
    https://leetcode.com/problems/design-compressed-string-iterator/description/
    letter-count,letter-count...
    StringIterator iterator = new StringIterator("L1e2t1C1o1d1e1");
    iterator.next(); // return 'L'
    iterator.next(); // return 'e'
    iterator.next(); // return 'e'
    iterator.next(); // return 't'
    iterator.next(); // return 'C'
    iterator.next(); // return 'o'
    iterator.next(); // return 'd'
    iterator.hasNext(); // return true
    iterator.next(); // return 'e'
    iterator.hasNext(); // return false
    iterator.next(); // return ' '
    """

    def __init__(self, compress_str):
        self.s = compress_str
        self.cur = ''
        # count用来计数当前char的剩余数量，pos记录的是compress_str对应的index
        # Edge case就是，如果出现a20的情况，需要parse 20为一个整体
        self.pos = self.count = 0

    def next(self):
        if not self.has_next():
            return ' '
        if self.count == 0:
            self.cur = self.s[self.pos]
            self.pos += 1
            while self.pos < len(self.s) \
                    and self.s[self.pos] in '0123456789':
                self.count = self.count * 10 + int(self.s[self.pos])
                self.pos += 1
        self.count -= 1
        return self.cur

    def has_next(self):
        return self.pos < len(self.s) or self.count > 0


def decode_string(s):
    """
    https://leetcode.com/problems/decode-string/description/
    给定一个词频压缩格式，还原成原始的string。
    s = "3[a]2[bc]", return "aaabcbc".
    s = "3[a2[c]]", return "accaccacc".
    s = "2[abc]3[cd]ef", return "abcabccdcdcdef".
    需要遍历每个char，判断是否为数字，还是[]，或者是letter，然后用Stack来表示当前需要解压的string，以及对应的个数
    """
    stack = list([["", 1]])  # [char, k]
    num = ""
    for c in s:
        if c.isdigit():
            # numbers 可能之后还有number，需要先加到num中去，继续找下一个
            num += c
        elif c == '[':
            # 那么此时num到头了
            stack.append(["", int(num)])
            num = ""
        elif c == ']':
            # 新的一个词频压缩结束，出栈后，更新新的top的string值
            st, k = stack.pop()
            stack[-1][0] += st * k
        else:
            # 单纯的字母，加入到stack top中的string去
            stack[-1][0] += c
    return stack[0][0]
