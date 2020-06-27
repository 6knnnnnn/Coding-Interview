# -*- coding: utf-8 -*-


def count_primes(n):
    """
    https://leetcode.com/problems/count-primes/description/
    找到从2到num之间，质数的个数。
    最简单的做法，对于2到num之间的数字，每次都判断是否为prime，最坏情况为O(N * M)，M为小于N的质数的个数，可以用空间优化
    1. 生成一个bit array，对于位置i的bit，1代表是prime，0代表不是prime
    从2到num开始遍历，如果i在bit array中是质数，那么对于所有i的倍数j，把j在bit array里面的bit变为0
    2. 生成一个hash set，初始化为所有2到num的数字，从2到num开始遍历，如果i还在set中，代表他是prime，把它所有的倍数都从set中删除
    """
    primes, count = set(range(2, n)), 0
    # for p, all p*x < n not prime
    for i in xrange(2, n):
        if i in primes:
            count, j = count + 1, 2
            while i * j in primes or i*j < n:
                if i * j in primes:
                    primes.remove(i * j)
                j += 1
    return count


count_primes(10)

def ugly_number(num):
    """
    https://leetcode.com/problems/ugly-number/description/
    :param num:
    :return:
    """


def ugly_num_2(first_n):
    """
    https://leetcode.com/problems/ugly-number-ii/description/
    找到前N个 ugly numbers
    :param first_n:
    :return:
    """