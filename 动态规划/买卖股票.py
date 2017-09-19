# -*- coding: utf-8 -*-


def buy_and_sell_1_transaction(prices):
    """
    https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
    找到最大利润的一个交易，可以预处理数组，也可以用一个变量记录，遍历到某个price为止，全局的最小值
    只记录min price，如果新的price比min price大则更新利润，否则更新min price
    """
    max_profit = 0
    if prices and len(prices) >= 2:
        min_price = prices[0]
        for p in prices[1:]:
            if p <= min_price:
                min_price = p
            else:
                max_profit = max(max_profit, p - min_price)
    return max_profit


def buy_and_sell_as_many_as_possible(prices):
    """
    https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/
    只要前一秒的价格小于后一秒的价格，就买进卖出，加到利润里，贪心策略。
    """
    profit = 0
    if len(prices) >= 2:
        # When to buy?  p[i-1]>p[i]<p[i+1]
        # When to sell? p[i-1]<p[i]>p[i+1]
        for i in xrange(len(prices) - 1):
            profit += max(0, prices[i + 1] - prices[i])
    return profit


def buy_and_sell_two_at_most(prices):
    """
    https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/description/

    """
