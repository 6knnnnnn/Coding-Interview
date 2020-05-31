class KVStore(object):
    def __init__(self):
        self.kv = dict([])

    def put(self, k, v, ts):
        if k not in self.kv:
            self.kv[k] = list([])
        self.kv[k].append((v, ts))

    def size(self):
        return len(self.kv)

    def sizeAll(self):
        size = 0
        for _, v in self.kv.items():
            size += len(v)
        return size

    def get(self, k, ts):
        if k not in self.kv:
            return None
        timedValues = self.kv.get(k)
        timedValues.sort(key=lambda x:x[1])

        if timedValues[0][1] > ts:
            return None

        for i in xrange(len(timedValues)-1):
            if timedValues[i][1] <= ts < timedValues[i+1][1]:
                #  better approach -> binary search
                return timedValues[i][0]

        return timedValues[-1][0]


def test1():
    store = KVStore()
    key = "key1"
    store.put(key, 5, 50)
    store.put(key, 6, 60)
    for i in xrange(1, 5):
        store.put(key, i, i * 10)
    for j in xrange(1, 12):
        ts = j*8
        print ts, store.get(key, ts)
            # print store.get(key, j * 8)

test1()