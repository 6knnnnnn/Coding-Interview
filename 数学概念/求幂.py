# -*- coding: utf-8 -*-


def pow_recur(x, n):
    # https://leetcode.com/problems/powx-n/description/
    # 暴力解法，O(N)时间，也就是一个loop，但可以记住之前的计算结果复用
    # 因为 X^N = (X*X)^n/2 = X^(N/2) * X^(N/2)
    # 那么如果知道了X^(N/2)，就不需要再次计算X^(N/2)了
    if n == 0:
        return 1
    if n < 0:
        # 负数的话，就是求x倒数的幂
        n, x = -n, 1 / x
    if n % 2 == 0:  # Even
        # 其实就是bottom-up来计算，最开始的时候x^2，之后x^4...
        return pow_recur(x * x, n / 2)
    # Odd
    return x * pow_recur(x * x, n / 2)


def pow_itera(x, n):
    """
    这里面每次记录X^(N/2)，避免重复运算
    如果N=2M+1，基数，X^N= X * X^(M) * X^(M)
    如果N=2M，偶数，X^N次幂= X^(M) * X^(M)
    所以需要一个缓存ans，如果N为基数，则先把多余的1个x乘到ans里面
    例子： x=2 n = 11，每次while loop：
    start 0. m = 11 ans = 2^1  x = 2^2
          1. m = 5  ans = 2^3  x = 2^4
          2. m = 2  ans = 2^3  x = 2^8
          3. m = 1  ans = 2^11 x = 2^16
    end   4. m = 0  ans = 2048 x = 2^16
    """
    m = abs(n)
    ans = 1.0
    while m:
        if m % 2 == 1:
        # 基数，比如11/2=5
            ans *= x
        x *= x
        m = m/2
    if n < 0: return 1 / ans # 为负数则返回倒数
    return ans


def power_of_base_loop(base, value):
    if value == 1:
        return True
    if value < base: # 此时不等于1
        return False
    while value >= base:
        if value % base == 0:
            value = value/base
        else:
            return False
    return True


def power_of_2(x):
    # https://leetcode.com/problems/power-of-two/description/
    if x <= 0:
        return False
    # 对于2^n，第一位为1，其他n-1位为0
    # 所以2^n - 1，第一位为0，其他为均为1
    # 此时去AND运算，必须是0，否则不是2^n
    return x & (x-1) == 0


def power_of_4(x):
    # https://leetcode.com/problems/power-of-four/description/
    # 除了必须是2的幂次方之外，4的幂次方满足，基数位置的bit为1，偶数位置为0
    # 比如4^0 = 1, 4^1 = 100, 4^2 = 10000
    # 所以用1010101010101010101010101010101来和4做AND，结果和x一样则满足4的幂次方
    # 0b1010101010101010101010101010101 = 0x55555555 = 1431655765
    if not power_of_2(x):
        return False
    return x & 0b1010101010101010101010101010101 == x


def power_of_3(x):
    # https://leetcode.com/problems/power-of-three/description/
    # 所以判断一个数X是否是power of N，可以看N的最高幂次是多少，比如如果是int且N=2，则最高2^31
    # 如果N=3 则 1162261467 is 3^19,  3^20 is bigger than 2^32-1
    # 之后再用这个最大值，对X取模运算是否为0，因为如果X=N^y，那么最大值对它取模一定为0
    max_3_power_int = 1162261467
    return x > 0 and max_3_power_int % x == 0
