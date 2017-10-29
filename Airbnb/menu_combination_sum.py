# -*- coding: utf-8 -*-

"""
 Given a menu of dishes with prices on it, you have certain amount of money.
 You want to use all of the money to buy different dishes.
 What are the combinations you could have?

 本质是combination sum，但要注意价格为double，不能直接用 == 比较
 1. 转成cents，即全部乘以100，这样可以作为int处理
 2. 设定精度epsilon，两个数相差小于epsilon就认为是相等
"""


def menu_combinations(menu_prices, target):
    # 所有数字为正，且可以有无穷多个，但是结果不能有重复的，candidates是一个list
    def dfs(res, menu_prices, path, target):
        # 找到一个path为结果，这里面0.5可以作为是允许的误差范围
        # 比如说如果有0.5美元没花出去，这个menu order也是可以接受的
        if 0 <= target <= 0.5:
            res.append(path)
        elif target > 0:
            for i, item in enumerate(menu_prices):
                # i 每次都从0开始，因为是无穷各组合可能，没有限制
                # 如果x比target还大，不需要再继续找后边的了，因为已经排好序
                name, price = item
                if price <= target:
                    # this guarantee path node is appended in increasing order
                    dfs(res, menu_prices[i:], path + [name], target - price)

    if not menu_prices or not target:
        return []
    res, path = [], []
    # Use DFS to record results，必须把candidates 排好序
    menu_prices.sort(key=lambda menu: menu[1])
    dfs(res, menu_prices, path, target)
    return res

a = [("salad", 2.99), ("burger", 2.99), ("lamb roll", 3.99)]
b = 6.0

print menu_combinations(a, b)
