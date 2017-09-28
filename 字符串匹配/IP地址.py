# -*- coding: utf-8 -*-

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
