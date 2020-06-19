from heapq import heappush, heappushpop


def find_top_k(data, k):
    topk = []
    for d in data:
        heappush(topk, d) if len(topk) < k else heappushpop(topk, d)
    topk.sort(key=lambda feature: (feature.count, feature.feature), reverse=True)
    return topk


class RequestedFeature(object):
    def __init__(self, feature, count):
        self.feature = feature
        self.count = count

    def __repr__(self):
        return "{}: {}".format(self.feature, self.count)

    def __lt__(self, other):
        # first compare count then feature name
        if self.count != other.count:
            return self.count < other.count
        return self.feature < other.feature


data = [2, 7, 9, 3, 0, 10, 44, 33, 88, 90, 3, 24, 10]
features = []
for d in data:
    f = RequestedFeature("f{}".format(d), d)
    features.append(f)
features.append(RequestedFeature("kun", 55))
features.append(RequestedFeature("liu", 55))
k = 4
print find_top_k(features, k)


# Top K toys
class Toy(object):
    def __init__(self, name):
        self.name = name
        self.quotesCount = 0

    def addOneQuote(self):
        self.quotesCount += 1

    def __repr__(self):
        return "{}: {}".format(self.name, self.quotesCount)

def compareToy(self, other):
    if self.quotesCount != other.quotesCount:
        return self.quotesCount < other.quotesCount
    return self.name < other.name

def popularNToys(topToys, toys, quotes):
    # process each toy in input toys
    toysDict = {toyName: Toy(toyName) for toyName in toys}

    # calculate the frequency of each toy in each quote, w/o duplicate in each quote
    for quote in quotes:
        words = quote.split(" ")
        history = set([])
        for word in words:
            word = word.lower()
            if word not in history:
                # if first time process this word as a toy's name
                history.add(word)
                if word in toysDict:
                    toysDict[word].addOneQuote()

    print toysDict
    # sort the list by the __cmp__ interface method
    toysList = []
    for _, toy in toysDict.items():
        if toy.quotesCount != 0:
            toysList.append(toy)
    toysList.sort(reverse=True, key=lambda toy: (toy.quotesCount, toy.name))

    # now find the topToys
    result = list([])
    topToys = min(topToys, len(toysList))
    for toy in toysList[:topToys]:
        result.append(toy.name)

    return result


toys = ["ana", "bet", "cet", "del", "eur"]

def test1():
    quotes = [
        "ana",
        "bet",
        "ana",
    ]
    print popularNToys(2, toys, quotes)


def test2():
    quotes = [
        "ana ana hahah",
        "bet has lol",
        "del bet sadad",
        "ads cet eur asdac",
        "bet del asd",
    ]
    print popularNToys(2, toys, quotes)


# test1()
test2()