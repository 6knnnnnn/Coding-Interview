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
            vL.pop()
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
    "abc" => false，除了e以外的字母均不行
    "1 a" => false，除了e以外的字母均不行
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
            # +-号：只能在第一个，或e的后边，"+2e-10" = > true
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
    其实还是回溯法DFS，每次需要知道：剩下的未处理的substr，剩余的ip位数（最多为4），上一轮修复的局部ip地址，全局结果

    """
    def dfs(remain_s, remain_d, prev_restored, global_ips):
        if len(remain_s) <= remain_d * 3:
            if remain_d == 0:
                # no more substr to process, add to global
                global_ips.append(prev_restored[:]); return
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
