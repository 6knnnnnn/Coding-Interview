# -*- coding: utf-8 -*-

"""
https://docs.python.org/2/library/random.html

Python中随机数 random.randint(x, y) x与y都是inclusive
Return a random integer N such that a <= N <= b

Python中从一个iterable里面选择随机元素，random.choice(iterable)
Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.


random.sample(iterable, length)
Return a k length list of unique elements chosen from the population sequence. Used for random sampling without replacement.
"""

import random

for i in xrange(10):
    print random.randint(1, 100), random.choice(range(100))
