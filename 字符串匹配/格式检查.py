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


def validate_ip_address(ip_address):
    pass