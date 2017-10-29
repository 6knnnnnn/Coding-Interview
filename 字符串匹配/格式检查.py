# -*- coding: utf-8 -*-


def compare_version_numbers(v1, v2):
    """
    https://leetcode.com/problems/compare-version-numbers/description/
    其实就是corner case比较多
    1. 按照.为分隔符split，去掉每个version的后缀0，因为1.0 = 1
    2. 依次比较split之后每一位的int，只要有不相等的，就返回结果
    3. 如果其中一个提前结束，比较长度
    """
    def remove_tail_zero(vL):
        while len(vL) > 0 and int(vL[-1]) == 0:
            vL.poll()
        return vL
    vL1 = remove_tail_zero(v1.split('.'))
    vL2 = remove_tail_zero(v2.split('.'))
    i = j = 0
    while i < len(vL1) and j < len(vL2):
        v1, v2 = int(vL1[i]), int(vL2[j])
        if v1 != v2:
            return -1 if v1 < v2 else 1
        i, j = i + 1, j + 1
    if len(vL1) == len(vL2):
        return 0 # 长度一样，每一位的数字也一样
    return -1 if len(vL1) < len(vL2) else 1


def valid_number(s):
    """
    https://leetcode.com/problems/valid-number/description/
    把所有edge case考虑进去
    "0" => true，纯数字
    " 0.1 " => true，有小数点，只有一个，e不能和.同时出现，小数点两侧至少有一个数字，"0." ".3"
    "abc" "1 a" => false，除了e以外的字母均不行
    "2e10" => true，只有一个e，e两侧必须有数字，e不能和.同时出现
    +-号：只能在第一个，或e的后边，"+2e-10" => true
    """
    s = s.strip()
    has_point = has_e = has_num = False
    num_after_e = True
    for i, c in enumerate(s):
        if c in '0123456789': # 纯数字
            has_num = num_after_e = True
        elif c == '.':
            if has_e or has_point:
                # e不能和.同时出现，且只能有一个
                return False
            has_point = True
        elif c == 'e':
            # 只能有一个e，前边必须有数字
            if has_e or not has_num:
                return False
            has_e = True
            num_after_e = False
        elif c == '-' or c == '+':
            # +-号：只能在第0个，或e的后边，"+2e-10" = > true
            if i != 0 and s[i - 1] != 'e':
                return False
        else:
            return False  # other cases
    # 如果到最后没有数字，或者有数字和e但是没有数字在e后边，则为False，否则True
    return has_num and num_after_e


"""
IP4V: no leading zeros, [0, 255], 4 digits by “.”
IP6V: each length <= 4, delimited by “:”, can have leading zeros or omit leading zeros, but in hex digits
"""


def validate_ip_address(ip):
    """
    https://leetcode.com/problems/validate-ip-address/description/
    判断一个ip地址是Ipv4还是Ipv6格式，如果都不是，返回Neither
    "172.16.254.1" -> IPv4
    "256.256.256.256" -> Neither (IP4最大为255)
    "2001:0db8:85a3:0:0:8A2E:0370:7334" -> IPv6
    "2001:0db8:85a3:0:0:8A2E:0370:733!"  -> Neither（存在非hex字符）
    其实就是先判断IP的长度，然后判断edge case
    """
    addresses = ip.split(".")
    if len(addresses) == 4:
        for add in addresses:
            # negative, non-num, leading zero
            if not add.isdigit() or (len(add) > 1 and add[0] == '0') or int(add) > 255:
                break
        # at the end of for loop
        else:
            return "IPv4"
    addresses = ip.split(":")
    hexs = set("0123456789abcdefABCDEF")
    if len(addresses) == 8:
        for add in addresses:
            if not add or len(add) > 4 or any(c not in hexs for c in add):
                break
        else:
            return "IPv6"
    return "Neither"


def restore_ip_addresses(ip):
    """
    https://leetcode.com/problems/restore-ip-addresses/description/
    给定一个没有分隔符的ipv4地址，尝试修复地址，并返回所有的可能，例子：
    25525511135 -> 255.255.11.135, 255.255.111.35，2552 -> 2.5.5.2
    其实还是回溯法DFS，每次需要知道：剩下的未处理的sub str，剩余的ip位数（最多为4），上一轮修复的局部ip地址，全局结果
    """
    def dfs(remain_s, remain_d, prev_restored, global_ips):
        if len(remain_s) <= remain_d * 3:
            if remain_d == 0:
                # no more substr to process, add to global
                global_ips.add(prev_restored[:]); return
            left = min(3, len(remain_s) - remain_d + 1) # left < = 3
            for i in xrange(left):
                # each digit < 255, no leading 0 of digit
                if (i == 2 and int(remain_s[:3]) > 255) or (i > 0 and remain_s[0] == '0'):
                    continue
                # 新生成一个修复的局部ip地址
                newly_restored = prev_restored + [remain_s[:i + 1]]
                new_remain_s = remain_s[i + 1:]
                dfs(new_remain_s, remain_d - 1, newly_restored, global_ips)

    results = list([])
    dfs(ip, 4, [], results)
    return results


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
            # 计算出每个word之间的space，假设此时能够整除，注意space count = word_count-1，因为是两两word之间的空格
            space_count = len(curr_line_words) - 1
            if space_count == 0:
                # 特殊情况，即当前line目前为止只有一个word，原因是：这唯一的word长度刚好为max width，或者长度不为max width
                # 但是和new word不能组成新的一行，所以把这个唯一的word加到结果的同时，还要加入必要的额外空格（即左对齐）
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
