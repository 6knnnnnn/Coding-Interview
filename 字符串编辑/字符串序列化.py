# -*- coding: utf-8 -*-

# http://www.lintcode.com/zh-cn/problem/strings-serialization/

# 需要考虑 连接符，转义符的处理


def text_justification(words, max_width):
    """
    https://leetcode.com/problems/text-justification/description/
    给定一组word，将所有的word按行打印，每一行满足Justification，也就是"居中对齐"
    words: ["This", "is", "an", "example", "of", "text", "justification."], max width=16，结果：
        "This    is    an",
        "example  of text",
        "justification.  "
    一个大的假设是，word不会超过max width。同时满足三个条件：
    1. 需要满足greedy approach，即每一行尽可能多的打印word
    2. 最后一行，或者中间行但是只有一个word，只需要向left对齐即可
    3. 对于中间行额外的空格，尽可能的平均的分配到每个word，如果不能够平均分配，多出来的空格仍需要平均分配到尽量左边的word
    比如4个word：如果额外6个空格，每个word之间平均2个空格；如果额外7个空格，每个word之间2个空格，但最左边的word后边多出1个空格
        如果额外8个空格，每个word之间2个空格，但最左边的"两个"word后边多出1个空格（也就是尽可能的把8-6=2个空格平均分配到左边）
    """
    # 最终结果res，当前line，当前line已经有的word的总长度
    res, curr_line_words, curr_line_words_len = [], [], 0
    for new_word in words:
        # 算上new word以及其长度，len(curr_line_words_len) 为当前所有word之间只有一个空格的数量，也就是空格的长度
        # 再加上当前line已经有的word的总长度，就是如果算上new word后与当前line所组成的最小的可能的长度（因为只有一个空格所以最小）
        if len(curr_line_words) + curr_line_words_len + len(new_word) <= max_width:
            # 没有超过max width
            curr_line_words.append(new_word)
            curr_line_words_len += len(new_word)
        else:
            # 否则，当前word不能加入当前line，需要处理当前line，而且初始化一个新的line，把当前word加到新的当前line里面
            total_space_len = max_width - curr_line_words_len
            # 计算出每个word之间的space，假设此时能够整除，注意space count = word_count-1，因为是word之间的空格
            space_count = len(curr_line_words) - 1
            if space_count == 0:
                # 特殊情况，即当前line目前为止只有一个word，原因是：这唯一的word长度刚好为max width，或者长度不为max width
                # 但是和当前的word不能组成新的一行，所以把这个唯一的word加到结果的同时，还要加入必要的额外空格（即左对齐）
                curr_line_str = curr_line_words[0] + ' ' * (max_width - len(curr_line_words[0]))
            else:
                # 先假设能够整除
                evenly_word_space = ' ' * (total_space_len / space_count)
                if total_space_len % space_count != 0:
                    # 如果不能整除，每个word之间的space除了evenly_word_space之外，还需要处理前边的需要多分配的word
                    # this is a b，4个word总长度=8，3个空格，所有空格的总长度=16-8=8，平均分布的空格长度 = 8/3 = 2
                    # 多出来的空格 = 8 - 2*3 = 2，那么前两个word多有一个空格
                    # 因为肯定小于word数量，所以可以从头开始，依次将当前line里已有word，在分配平均空格的基础上，再多给一个空格
                    extra_spaces_count = total_space_len - len(evenly_word_space) * space_count
                    for so_far in xrange(extra_spaces_count):
                        curr_line_words[so_far] += ' '
                curr_line_str = evenly_word_space.join(curr_line_words)
            res.append(curr_line_str)
            # 把当前word加入到新的一行中去
            curr_line_words = [new_word]
            curr_line_words_len = len(new_word)
    # 对于最后一行，特殊处理一下while loop结束后的curr_line_so_far_words（因为这些word没有超过max width就结束了）
    last_line_str = ' '.join(curr_line_words)
    if len(last_line_str) < max_width:
        # 额外的补空格到最后一行中去，左对齐
        last_line_str += ' ' * (max_width - len(last_line_str))
    res.append(last_line_str)
    return res


def test1():
    tests = [
        (["this", "is", "a", "long", "areallylongone"], 16),
        (["this", "is", "a", "log", "last", "one"], 16),
        (["this", "is", "a", "b", "second", "last", "one"], 16),
        (["this",  "is",  "a",  "long"], 16),
        (["a","b","c","d","e"], 1),
        (["Listen","to","many,","speak","to","a","few."], 6)
    ]

    real = [["this  is  a long", "areallylongone  "],
            ["this  is  a  log", "last one        "],
            ["this   is   a  b", "second last one "],
            ["this is a long  "],
            ["a", "b", "c", "d", "e"],
            ["Listen", "to    ", "many, ", "speak ", "to   a", "few.  "] # 第2、3、4行只有1个word
        ]

    for i, test in enumerate(tests):
        compare = real[i]
        if i != 5:
            continue
        result = text_justification(test[0], test[1])
        if len(result) != len(compare):
            print "行数不一样", test
        else:
            for j in xrange(len(result)):
                if result[j] != compare[j]:
                    print i, "\n", len(result[j]), result[j], "\n", len(compare[j]), compare[j], "\n----------"


def caesar_cipher(s, k):
    """
    凯撒密码 https://en.wikipedia.org/wiki/Caesar_cipher
    abc + 2 -> cde, a + 26 -> a, a + 27 -> b, xyz + 2 -> zab
    """
    res = list([])
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for c in s:
        i = (ord(c) - 97 + k) % 26
        res.append(alphabet[i])
    return "".join(res)
