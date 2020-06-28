def paintHouse(n, k):
    dp = [0] * (n + 1)
    dp[1] = k
    for i in xrange(2, n+1):
        # same as previouse house
        countSameAsPrev = dp[i-1]
        countDiffAsPrev = (k-1) * dp[i-1]
        dp[i] = countSameAsPrev + countDiffAsPrev
        # dp[i] = dp[i-1] + dp[i-1] * (k-1)
        # dp[i] = dp[i-1] * k

    return dp


def paintHouseSpace(n, k):
    if n <= 1:
        return k * n
    prev = k
    total = 1
    for _ in xrange(2, n+1):
        total = prev * k
        prev = total
    return total

print paintHouse(3, 4)
print paintHouseSpace(3, 4)


def paintHouse3Colors(costs):
    accuR, accuG, accuB = 0, 0, 0
    # costs = [ (1, 2, 3), (4, 3, 2) ...]
    for c in costs:
        currHouseR = c[0] + min(accuG, accuB)
        currHouseG = c[1] + min(accuB, accuR)
        currHouseB = c[2] + min(accuR, accuG)
        accuR, accuG, accuB = currHouseR, currHouseG, currHouseB
    return min(accuB, min(accuG, accuR))




