# -*- coding: utf-8 -*-


def count_and_say(total):
    """
    https://leetcode.com/problems/count-and-say/description/
    1, 11, 21, 1211, 111221, 312211, 13, 112221, 213211
    不可能出现三个连续的3，因为如果x333，说明之前有连续的3+x个3，或者如果333x，说明之前的数字是333 xxx，但不可能存在连续三个3
    也不可能出现4、5、6... 最多2个3，可以有3个2或者1
    暴力解法，每次遍历num的所有数位，如果跟之前的一样，就继续，否则计数完毕
    """
    num = "1"
    for i in xrange(total - 1):
        res, prev, count = [], num[0], 0
        for n in num:  # check each num
            if prev == n:
                count += 1
            else:
                # 当前一组连续的计数完毕，开始下一个n
                res.append("%s%s" % (count, prev))
                prev, count = n, 1
        # 关键点：把最后的连续数位加进去
        res.append("%s%s" % (count, prev))
        num = "".join(res)
    return num
