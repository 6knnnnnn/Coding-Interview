# -*- coding: utf-8 -*-


def int_to_roman(num):
    values = [1000, 900, 500, 400,
              100, 90, 50, 40, 10,
              9, 5, 4, 1]
    chars = ['M', 'CM', 'D', 'CD',
             'C', 'XC','L', 'XL', 'X',
             'IX', 'V', 'IV', 'I']
    res_list = list([])
    # 不断地减，每一位都找最多，贪心
    for i in xrange(len(values)):
        while num >= values[i]:
            num -= values[i]
            # 找到对应的罗马字符
            res_list.append(chars[i])

    return ''.join(res_list)


test1 = [1, 2, 4, 5, 9, 10, 11]

for t in test1:
    print t, int_to_roman(t)


def roman_to_int(roman_str):
    roman = {'M': 1000, 'D': 500,
             'C': 100, 'L': 50,
             'X': 10, 'V': 5, 'I': 1}
    num = 0
    for i in xrange(len(roman_str) - 1):
        c1, c2 = roman_str[i], roman_str[i + 1]
        # 根据c1 c2是否升序，来判断加减c1
        if roman[c1] < roman[c2]: # IV=4 I=1<V=5
            # 先减去小的，之后会加上大的，即累加大减小
            num -= roman[c1]
        else:
            num += roman[c1]
    return num + roman[roman_str[-1]]

test2 = ["MD", "IC", "IL", "XL", "XX", "XV"]

for t in test2:
    print t, roman_to_int(t)