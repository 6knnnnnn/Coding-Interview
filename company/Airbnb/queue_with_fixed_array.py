# -*- coding: utf-8 -*-
"""
 Implement a queue with fixed-size arrays (or arraylist)

 Solution: Use the last position of the array to store the next array

 If deque, also need to support stack way -> FILO
"""


class MyQueue(object):
    def __init__(self, size):
        self.size = size
        self.tail = self.head = self.count = 0
        self.array = [None] * size

    def clear(self):
        self.array = [None] * self.size
        self.head = self.tail = self.count = 0

    def add(self, value):
        if self.count == len(self.array):
            raise Exception("No more space to add")
        # move tail forward until the end
        self.array[self.tail] = str(value)
        self.tail += 1
        if self.tail == self.size:
            self.tail = 0
        self.count += 1
        return True

    def poll(self):
        if self.count > 0:
            data = self.array[self.head]
            self.array[self.head] = None
            self.count -= 1
            self.head += 1
            # move forward until the end
            if self.head == self.size:
                self.head = 0
            return data
        else:
            raise Exception("No more element to poll")

    def is_empty(self):
        return self.count == 0

    def __repr__(self):
        return "head=%s, tail=%s" % (self.head, self.tail)

queue = MyQueue(5)

queue.add(1)
queue.add(2)
queue.add(3)
queue.add(4)
queue.add(5)
print queue.poll() # 1
print queue.poll() # 2
queue.add(6)
while not queue.is_empty():
    print queue.poll()