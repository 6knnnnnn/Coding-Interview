# -*- coding: utf-8 -*-

"""
两个字符串一样长的时候，说明有一个替换操作，我们只要看对应位置是不是只有一个字符不一样就行了
一个字符串比另一个长1，说明有个增加或删除操作，我们就找到第一个对应位置不一样的那个字符
如果较长字符串在那个字符之后的部分和较短字符串那个字符及之后的部分是一样的，则符合要求
如果两个字符串长度差距大于1，肯定不对
"""


def is_one_edit_distance(s, t):
    # https://leetcode.com/problems/one-edit-distance/description/
    def is_one_modified(s, t):
        modified = False
        for i in xrange(len(t)):
            if s[i] != t[i]:
                if modified: # 第二次modified了
                    return False
                modified = True
        return modified

    def is_one_delete(longer, short):
        for i in xrange(len(short)):
            if longer[i] != short[i]:
                # the 1st different, compare the rest
                return longer[i + 1:] == short[i:]
        return True

    if abs(len(s) - len(t)) > 1: return False
    if len(s) == len(t):  # same length
        return is_one_modified(s, t)
    return is_one_delete(s, t) if len(t) < len(s) \
        else is_one_delete(t, s)

