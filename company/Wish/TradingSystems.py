# implement a trading system which has the following components:
#
# 1. buy(num_of_product, price)
# Called by buyer to buy certain numbers of products with a maximum price
# num_of_product (INTEGER): numbers of products to buy
# price (FLOAT): maximal price/unit the buyer is willing to pay
# Return (INTEGER): numbers of products can be bought
#
# 2. sell(num_of_product, price)
# Called by seller to sell certain numbers of products with a minimum price
# num_of_product (INTEGER): numbers of products to sell
# price (FLOAT): minimal price/unit the seller is willing to sell
# Return (INTEGER): numbers of products can be sold
#
# Examples:
#
# system = TradingSystem()
# system.sell(50, 1.5)
# return: 0
#
# system.sell(20, 1.4)
# return: 0
#
# system.buy(60, 1.51)
# return: 60
#
# system.buy(20, 1.5)
# return: 10
#
# system.sell(20, 0.7)
# return: 10
#
# system.buy(100, 0.6)
# return: 0
from heapq import heappush, heappop


class Product(object):
    def __init__(self, price, num):
        self.price = price
        self.num = num

    def __lt__(self, other):
        return -self.price < -other.price

    def __repr__(self):
        return "price={} num={}".format(self.price, self.num)


class TradingSystem(object):
    def __init__(self):
        self.sellPQ = list([])
        self.buyPQ = list([])

    def processTransaction(self, isBuy, num, price):
        outPQ = self.sellPQ if isBuy else self.buyPQ
        inPQ = self.buyPQ if isBuy else self.sellPQ
        outCount = 0
        overpriceList = []
        while outCount < num and outPQ:
            product = outPQ[0]
            if product.price > price:
                overpriceList.append(product)
                heappop(outPQ)
            else:
                if outCount + product.num <= num:
                    outCount += product.num
                    heappop(outPQ)
                else:
                    product.num -= num - outCount
                    outCount = num
        if outCount < num:
            heappush(inPQ, Product(price, num - outCount))
        for product in overpriceList:
            heappush(outPQ, product)
        return outCount

    def buyV2(self, num, price):
        return self.processTransaction(True, num, price)

    def buy(self, num, price):
        boughtCount = 0
        overpriceList = []
        while boughtCount < num and self.sellPQ:
            product = self.sellPQ[0]
            if product.price > price:
                # if this product is too expensive, save it to cannot buy list
                overpriceList.append(product)
                heappop(self.sellPQ)
            else:
                # a deal can be made, update boughtCount + sellPQ based on sold out or not
                if boughtCount + product.num <= num:
                    # this product is sold out
                    boughtCount += product.num
                    heappop(self.sellPQ)
                else:
                    # this product not sold out
                    product.num -= num - boughtCount
                    boughtCount = num
        if boughtCount < num:
            # remained some buys
            heappush(self.buyPQ, Product(price, num-boughtCount))
        for product in overpriceList:
            heappush(self.sellPQ, product)

        return boughtCount

    def sell(self, num, price):
        return self.processTransaction(False, num, price)


ts = TradingSystem()
for p, n in [(1.6, 30), (1.4, 20), (1.5, 40)]:
    ts.sell(n, p)

print ts.sellPQ
for p, n in [(1.51, 30), (1.4, 20), (1.7, 50)]:
    print ts.buyV2(n, p)
    print ts.sellPQ

print ts.buyPQ