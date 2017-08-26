# -*- coding: utf-8 -*-

# 做法有很多，排序，hash table，但如何做到O(N)时间，O(1)空间？
# 如果把所有数字看成一个整体都是binary表达的方式，其实是一个bit map，或者说bit matrix


def single_number_twice(nums):
    """
    https://leetcode.com/problems/single-number/description/
    对于任意两个相同的数字的每一个bit位，异或运算结果均为False
    对于任意两个不同的数字的每一个bit位，异或运算结果看情况，00或者11就是0，否则1
    如果对所有数字进行位运算，每一个bit位所留下来的结果，就是那个只出现了一次的数字T的对应bit位
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
    建立一个32位的数字，来统计每一位上1出现的个数，如果某一位上为1+该整数出现了三次，对3去余为0
    所以，把每个数的对应位都加起来对3取余，最终剩下来的那个数就是单独的数字
    """
    def convert(bit_map):
        res = 0
        total = len(bit_map)
        for i, b in enumerate(bit_map):
            if b == 1 or b == '1':
                res += 2 ** (total - i - 1)
        return res
    bit_map = [0]*32
    for i in xrange(32):
        bit_sum = 0
        for n in nums:
            # 找到所有数字对应i位置的1的个数，累加到bit sum中
            # (n >> i) & 1 就是数字n对应i位置的1
            bit_sum += (n >> i) & 1
        # 对所有出现次数为3的数字，对应i位置的1的累加和肯定是3的倍数
        # 所以bit_sum % 3就是那个只出现了一次的数的对应bit位置的数（非0即1）
        bit_map[i] = bit_sum % 3
    return convert(bit_map[::-1])


nums = [-2,-2,1,1,-3,1,-3,-3,-4,-2]
print single_number_third(nums)