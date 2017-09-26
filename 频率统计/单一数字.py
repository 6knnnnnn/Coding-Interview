# -*- coding: utf-8 -*-

# 做法有很多，排序，hash table，但如何做到O(N)时间，O(1)空间？
# 如果把所有数字看成一个整体都是binary表达的方式，其实是一个bit map，或者说bit matrix


def single_number_twice(nums):
    """
    有一个数字只出现了一次，其他的都出现了两次，找到这个single number
    https://leetcode.com/problems/single-number/description/
    对于任意两个相同的数字的每一个bit位，异或运算结果均为False
    对于任意两个不同的数字的每一个bit位，异或运算结果看情况，00或者11就是0，否则1
    如果对所有数字的每一位进行XOR运算，每一个bit位所留下来的结果，就是那个只出现了一次的数字T的对应bit位
    因为出现了两次的数字，bit位XOR后为只可能为0，此时再跟只出现了一次的T的对应bit位XOR后，如果T是1则还是1，为0则还是0
    0 0 0 1 1 0 1 0 XOR 0 0 0 1 1 0 1 0 =  0 0 0 0 0 0 0 0，再次 XOR 1 0 0 1 0 1 0 1 = 1 0 0 1 0 1 0 1自己
    对于出现了两次的数字的每一个bit位，多次进行XOR也没关系，最后都会是0
    """
    res = 0
    for n in nums:
        res ^= n
    return res


def single_number_third(nums):
    """
    https://leetcode.com/problems/single-number-ii/description/
    所有均出现了3次，只有一个出现了一次
    建立一个32位的数字，来统计每一位上1出现的个数，如果是3的倍数，即取余为0，表明此位置是重复了3次的bit；否则，只可能为1
    所以，把每个数的对应位都加起来对3取余，最终剩下来的那个数就是单独的数字
    时间复杂度O(N)，这道题目用python写就会遇到负数的问题，Java写同样的代码就没有问题。
    """
    res = 0
    for i in xrange(32):
        bit_sum = 0
        for n in nums:
            # (n >> i) & 1 就是数字n对应i位置的bit值
            if (n >> i) & 1 == 1:
                bit_sum += 1
        # bit_sum % 3 即如果bit sum是3的倍数则为0，否则只可能为1，因为假设是只出现了一次的数字
        bit_sum = bit_sum % 3
        if bit_sum:
            # 位或运算 |，即两个数字的同一位只要有一个1，两个数字在该位的|就是1
            # res最开始是0，即每一位都是0，只要有ith bit是1，就变为1
            res |= bit_sum << i
    return res

nums = [2,2,1,1,3,1,3,3,4,2]
print single_number_third(nums)