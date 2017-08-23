# -*- coding: utf-8 -*-
import random


def random_5_to_7():
    # 只有一个能生成1到5的随机数的API，如何实现找到1到7的随机数的方法？
    # 二进制随机元：先通过random5 API生成一个数，其中[1,2]代表0，[3,4]代表1，[5]代表重新随机
    # 每次生成log7长度的随机0或者1，如果都是0，代表需要重新随机，否则就是随机的结果
    # 扩展1：只有能生成1到M的随机数的API，如何实现1到N的随机数方法（M<N）？
    # 同理，randomM API 生成[1..M/2]代表0，如果M为基数，[M]代表重新随机，[M/2+1...M-1]代表1，否则[M/2+1...M]代表1
    # 扩展2：生成[X...Y]的随机数？其实可以用二进制随机元生成一个[0, Y-X]的数字，之后再加上X作为offset
    def random_5_api():
        return random.randint(1, 5)
    length = len(bin(7)) - 2 # bin(7) = 0b111
    bin_random_num = list([])
    while length > 0:
        rnd = random_5_api()
        if rnd == 5:
            continue
        if 1 <= rnd <= 2:
            bin_random_num.append('0')
        else: # 3 <= rnd <= 4:
            bin_random_num.append('1')
        length -= 1
    int_num = int(''.join(bin_random_num), 2)
    # 如果目标是实现随机生成[0, 7]的数字，生成的二进制都是0也可以当做是结果
    return int_num if int_num != 0 else random_5_to_7()


def equal_random_binary_simulate():
    # 已知一个API可以随机生成0或者1，但是概率不等，要求只通过这个API来实现等概率生成0和1的方法？
    # 两次调用API，看得到的结果是什么，如果是00或者11，重新再次随机
    # 否则如果是01返回0，如果10，则返回1
    # 证明：无论p为多少，两次随机返回01和10的概率都是p(1-p)，所以根据01和10来代表返回0还是1，即binary随机
    def not_equal_random_binary(p=0.4):
        # p = 返回1的概率，比如40%，那么有40%概率返回1
        rnd = random.randint(1, 100)
        return 1 if rnd > 100*p else 0
    rnd1 = not_equal_random_binary()
    rnd2 = not_equal_random_binary()
    if rnd1 == 1 and rnd2 ==0:
        return 1
    if rnd1 == 0 and rnd2 == 1:
        return 0
    return equal_random_binary_simulate() # 重做

for i in xrange(100):
    print equal_random_binary_simulate()
