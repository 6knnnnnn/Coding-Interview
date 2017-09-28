# -*- coding: utf-8 -*-


"""
如果是min heap，直接用heapq，如果需要max heap，最好用PriorityQueue，或者把key取负号，比如数值型就加负号
Python里面使用优先队列/heap的方法：
1. from heapq import xxx
基本操作：默认是min heap，如果是max heap，可以把priority异号，即变成它的相反数（假设是数值型的）
    heapify(list_x): 把list x 转换为一个heap，inplace O(N)时间
        一般默认list_x里面每个元素是一个tuple，里面第一个元素是priority，即(priority, other fields...)
        _heapify_max，即返回一个max heap
    heappush(heap_x, item): 把item push到heap_x里面，保持heap_x的属性（假设heap_x是合法的）
    heappop(heap_x): 把heap_x里面的最小元素pop出来，如果为空抛出异常。如果只是读取最小元素，直接heap_x[0]
组合操作：比单独操作更高效，但需要注意顺序
    heappushpop(heap_x, item)，push item to heap_x and after that, pop the smallest one
    heapreplace(heap_x, item)，跟heappushpop刚好相反
    nlargest/nsmallest(k, iterable_x, [key])，找到最大或者最小的，适合k比较小的情况，如果k=1最好用min/max，k很大最好sort

2. from Queue import PriorityQueue
    put(item)，把item放入到当前object中，假设tuple的第0个元素是priority
        如果item实现了__cmp__(other)，PQ就会根据这个__cmp__来比较（tuple类默认的__cmp__就是比较第0个元素）
    get()，返回top element，即min heap返回最小值，max heap返回最大值
    empty() 判断当前object是否为空
"""

from Queue import PriorityQueue

q = PriorityQueue(maxsize=10)

q.put([10, 'ten'])
q.put((1, 'one'))
q.put((5, 'five'))

while not q.empty():
    print q.get()
