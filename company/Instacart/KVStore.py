from collections import defaultdict


class TimeMap(object):

    def __init__(self):
        self.data = defaultdict(list)

    def set(self, key, value, timestamp):
        self.data[key].append((value, timestamp))

    def getExact(self, key, timestamp):
        if key not in self.data:
            return None
        values = self.data[key]
        # do binary search on values based on ts
        l, r = 0, len(values) - 1
        while 0 <= l <= r < len(values):
            mid = (l + r) / 2
            if values[mid][1] == timestamp:
                return values[mid][0]
            elif values[mid][1] < timestamp:
                l = mid + 1
            else:
                r = mid - 1
        return None

    def getCloest(self, key, timestamp):
        values = self.data[key]
        if timestamp > values[-1][1]:
            return values[-1]
        if timestamp < values[0][1]:
            return ""
        # now the result should be in the middle of the values, if exists
        l, r = 0, len(values) - 1
        while 0 <= l <= r < len(values):
            mid = (l + r) / 2
            if values[mid][1] == timestamp:
                # exact match
                return values[mid]
            elif mid - 1 >= 0 and values[mid-1][1] < timestamp < values[mid][1]:
                # in the left range
                return values[mid-1]
            elif mid + 1 < len(values) and values[mid][1] < timestamp < values[mid+1][1]:
                # in the right range
                return values[mid]
            # not found, next BS
            if values[mid][1] < timestamp:
                l = mid + 1
            elif values[mid][1] > timestamp:
                r = mid - 1
        return ""


def testGetExact():
    tm = TimeMap()
    tm.set("key1", "v1", 1)
    tm.set("key1", "v4", 4)
    tm.set("key1", "v6", 6)
    tm.set("key1", "v9", 9)
    for i in xrange(12):
        print i, tm.getExact("key1", i)


def testGetCloset():
    tm = TimeMap()
    tm.set("key1", "v1", 1)
    tm.set("key1", "v4", 4)
    tm.set("key1", "v6", 6)
    tm.set("key1", "v9", 9)
    for i in xrange(12):
        print i, tm.getCloest("key1", i)


# testGetCloset()
a = [
    ("v1", 1), ("v1", 21), ("v1", 11), ("v1", -11), ("v1", 10)
]

a.sort(key=lambda x : x[1])
print a
