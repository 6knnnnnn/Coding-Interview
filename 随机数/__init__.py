# -*- coding: utf-8 -*-

"""
Python中随机数 random.randint(x, y) x与y都是inclusive
Python中从一个iterable里面选择随机元素，random.choice(iterable)
"""

import random

for i in xrange(10):
    print random.randint(1, 100), random.choice(range(100))
