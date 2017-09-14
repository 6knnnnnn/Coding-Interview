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
