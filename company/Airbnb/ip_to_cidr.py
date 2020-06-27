# -*- coding: utf-8 -*-
"""
将一个ip range 转化为一组CIDR 地址

"""


def ipToVal(ip):
    # 256-based numbers to 10-based, e.g. 255.0.0.7 -> 4278190087
    ip = ip.split(".")
    val = 0
    for x in ip:
        val = (val << 8) + int(x)
    return val


def ValToIp(val):
    ip, i = ["0"] * 4, 3
    step = (1 << 8)
    while val:
        ip[i] = str(val %  step)
        val /= step
        i -= 1
    return ".".join(ip)


ip = "255.0.0.7"

a = ipToVal(ip)
b = ValToIp(a)

print a, b