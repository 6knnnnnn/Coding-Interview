# -*- coding: utf-8 -*-


def convert(bit_map, negative):
    # 给定一个bit map，把它转化为对应的int，bit map不一定是32位的
    # 比如 '101' 就是 4+1=5
    res = 0
    total = len(bit_map)
    for i, b in enumerate(bit_map):
        if b == 1 or b == '1':
            # 需要-1，因为最后一位如果是1则是2^(1-1)=2^0=1，如果是0则为0
            res += 2 ** (total - i - 1)
    return -res if negative else res


for i in xrange(-1000, 1000):
    bit_map = list(str(bin(i))[2:])
    res = convert(bit_map, i<0)
    if res != i:
        print res, i, bit_map
