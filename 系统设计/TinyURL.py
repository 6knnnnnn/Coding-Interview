# -*- coding: utf-8 -*-


class TinyURL(object):
    """
    https://leetcode.com/problems/encode-and-decode-tinyurl/description/
    设计一个简单的tiny URL服务，具体实现方式不重要，只要decode和encode的方法能够返回同一个URL即可
    用两个map，分别是index->url以及 url->index，每次新增一不存在的个url，index就是map的大小
    空间O(N)，时间O(1)。这道问题的关键点就是，如何去重复hash map可以跟好的解决
    follow up，如果空间有限，如何优化？
        如果有过期机制，而且是越早加进来的越早过期，那么可以用一个queue
        如果根据最近使用时间，比如最近使用过的晚过期，那么可以用LRU的方式
        如果根据总共使用频率，可以用LFU
    """
    def __init__(self):
        self.url_index = dict([])
        self.index_url = dict([])

    def encode(self, long_url):
        if long_url not in self.url_index:
            index = len(self.url_index)
            self.url_index[long_url] = index
            self.index_url[index] = long_url
        return str(self.url_index[long_url])

    def decode(self, short_url):
        j = int(short_url)
        return self.index_url.get(j)
