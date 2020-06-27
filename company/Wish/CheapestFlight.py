# -*- coding: utf-8 -*-
from collections import deque


class CityCost(object):
    def __init__(self, cityID):
        self.cityID = cityID
        self.directFlights = {}
        self.globalMinCostFromSrc = float('inf')

    def addDirectFlight(self, toCity, price):
        self.directFlights[toCity] = price

    def __repr__(self):
        df = ""
        for c, p in self.directFlights.items():
            df += "to {}, price {}".format(c, p)
        return "ID={} DF: {}".format(self.cityID, df)


class Solution(object):
    def findCheapestPrice(self, n, flights, src, dst, K):
        graph = {}
        # build graph + flight info
        for flight in flights:
            fromCity, toCity, price = flight
            if fromCity not in graph:
                graph[fromCity] = CityCost(fromCity)
            if toCity not in graph:
                graph[toCity] = CityCost(toCity)
            graph[fromCity].addDirectFlight(graph[toCity], price)

        # queue = for a given stop i, the min cost from src to this city
        queue, i = deque([(graph[src], 0)]), 0
        while queue and i <= K:
            i += 1
            for _ in xrange(len(queue)):
                fromCity, minCostFromSrc = queue.popleft()
                for toCity, price in fromCity.directFlights.items():
                    newCostFromSrcStopK = minCostFromSrc + price
                    if toCity.globalMinCostFromSrc > newCostFromSrcStopK:
                        toCity.globalMinCostFromSrc = newCostFromSrcStopK
                        queue.append((toCity, newCostFromSrcStopK))
        # 因为i > K，此时的dst globalMinCostFromSrc一定是想要找的K stops之内的min cost
        res = graph.get(dst).globalMinCostFromSrc
        return -1 if res == float('inf') else res

    def findCheapestPriceDP(self, n, flights, src, dst, K):
        """
        DP[stop i][city j] -> from src to city j, i stop at most, the min cost
        DP[i][src] -> from src to src, no matter i, all 0 cost
        DP[K+2][dst] -> from src to dst, K stops at most (src->.. K stops..->dst), the min cost
        """
        # from src to src, no matter how many stops, 0 cost
        dp = [[0 if i == src else float('inf') for i in xrange(n)] for _ in xrange(K+2)]

        for i in xrange(1, K+2):
            for fromCity, toCity, price in flights:
                # 从src，经过本次fromCity到达toCity的成本 既考虑 src -> i-1 -> fromCity -> toCity
                # 和已知的从src不经过fromCity到达toCity的成本比较 i.e. src -> i -> toCity
                newCostFromCity = dp[i-1][fromCity] + price
                dp[i][toCity] = min(dp[i][toCity], newCostFromCity)

        return -1 if dp[K+1][dst] == float('inf') else dp[K+1][dst]


n = 4
flights = [[0,1,1],[0,2,5],[1,2,1],[2,3,1]]
src = 0
dst = 3
k = 1

print Solution().findCheapestPrice(n, flights, src, dst, k)
print Solution().findCheapestPriceDP(n, flights, src, dst, k)



