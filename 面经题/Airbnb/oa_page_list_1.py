# -*- coding: utf-8 -*-

"""
先根据page size和总共的house数量，定义所需要的page number，可能存在最后的page打印出house数量小于page size的情况

这里面我们引入"唯一分页"的概念：如果house没有重复，或者重复的数量<=还没有满的page数量，那么我们可以把这个house唯一的分布到每个page中。
（为什么要考虑没有满的page？满了就不能把house分配到这个page了）

如果一个house越多重复，越有可能不是"唯一分页"的house，所以，我们需要优先处理重复数多的house，因为重复数越少，越好处理
比如house只有1个，随便放，而如果是很多个，要提前知道。

另一方面，我们想要找到那些可以唯一分页的house，优先打印他们，也就是优先把他们放到最前边的page去，后边的page有重复也没事，我们尽力了。
而对于那些不是唯一分页的house，不管我们怎么分页他们，总会出现某个page有重复house的情况，所以干脆就"消极"的把他们放到最后的page打印。

当知道了house的重复数，我们贪婪的去优先处理那些可以唯一分页的，而且是优先处理那些重复数目比较多的house。
这样我们可以尽可能多的得到不包含重复的page，而且这些page尽可能的在前边。在这之后，再处理那些一定会重复的house，在后边的page打印。

具体算法：先按照count来分配到对应的page，再对每个page里面的house按照input index来打印
1. 根据输入，parse成house实体类，注意这里我们需要知道house的原始input index，以及一个关于house id -> list of house info的map
2. 根据输入，parse成page实体类，我们这里也是有一个page array作为最后打印的output（根据index顺序打印）
    同时还需要知道每次从哪个page开始，因为可能最上边的page已经满了，还有就是没有满的available page number
3. 把house实体类按照count从大到小排序，即按照重复数量从大到小处理：
    1）如果house的重复数 <= available page number，说明这个house对于当前没有满的page来说，是可以唯一分页的
        此时，从最上边的没有满的page开始，把house按照原始的input index，加入到每个page
        （page的总数肯定够用，因为提前计算好了page数目，不可能越界，但是每次加入house到page中去，最上边的page可能会提前变满）
    2）否则，说明对于当前所有page来说，无论怎么分，都无法满足唯一分页的情况，把他们加入到一个待处理list中去
4. 所有的可唯一分页的house处理完之后，剩下的不能唯一分页的house，从最上边的page开始，依次加入到page里
5. 最后打印的时候，需要把page list里面每个page所包含的house按照input index来排序，即按照原始输入来打印

"""
from collections import defaultdict


class House(object):
    def __init__(self, house_id, list_id, points, city, input_index):
        self.house_id = house_id
        self.list_id = list_id
        self.points = float(points)
        self.city = city
        self.input_index = input_index

    def __repr__(self):
        return "%s,%s,%s,%s" % (self.house_id, self.list_id, self.points, self.city)

    def __str__(self):
        return "%s: %s" % (self.input_index, self.house_id)

    def __cmp__(self, other):
        # used to compare two houses by points
        return self.input_index - other.input_index

    @staticmethod
    def parse_input_as_houses(lines):
        # Parse each line, create a house entity, return a dict with key = house id -> value = a list of house entity
        house_info_dict = defaultdict(list)
        for i, line in enumerate(lines):
            data = line.split(",")
            if data and len(data) == 4:
                house_info = House(data[0], data[1], data[2], data[3], i)
                house_info_dict[data[0]].append(house_info)
        return house_info_dict

    @staticmethod
    def sort_house_id_by_count(house_info_dict):
        house_count_list = list([])
        total_count = 0
        for house_id, house_list in house_info_dict.items():
            count = len(house_list)
            total_count += count
            house_count_list.append((count, house_id))
        house_count_list.sort(reverse=True)
        return total_count, house_count_list


class Page(object):
    def __init__(self, page_size):
        self.house_list = list([])
        self.page_size = page_size
        self.house_id_set = set([])

    def add_house(self, house):
        self.house_list.append(house)
        self.house_id_set.add(house.house_id)

    def contains_duplicate(self):
        return len(self.house_list) != len(self.house_id_set)

    def __repr__(self):
        return "%s total, %s unique" % (len(self.house_list), len(self.house_list))

    def is_page_full(self):
        return len(self.house_list) == self.page_size

    @staticmethod
    def print_pages(page_array):
        # sort house in a page by its original input index then print it
        for page in page_array:
            for house in page.house_list:
                print house
            print ""

    @staticmethod
    def create_page_list(page_size, total_house_count):
        total_page_count = total_house_count/page_size
        if page_size != 1 and total_page_count * page_size < total_house_count:
            total_page_count += 1
        return list([Page(page_size) for _ in xrange(total_page_count)])

    @staticmethod
    def is_unique_pageable(house_count, page_list, first_available_page_index):
        return house_count <= (len(page_list) - first_available_page_index)

    @staticmethod
    def assign_house_to_pages_vertically(target_house_list, page_list, start_page_index):
        # now we could assign all houses in house_list to all pages starting from the first available page vertically
        for house in target_house_list:
            page_list[start_page_index].add_house(house)
            start_page_index += 1

    @staticmethod
    def assign_house_to_pages_sequentially(target_house_list, page_list, start_page_index):
        for house in target_house_list:
            if page_list[start_page_index].is_page_full():
                while page_list[start_page_index].is_page_full():
                    start_page_index += 1
            page = page_list[start_page_index]
            page.add_house(house)

    @staticmethod
    def split_pages(page_list):
        unique_page_list, duplicate_page_list = list([]), list([])
        for page in page_list:
            if page.contains_duplicate():
                duplicate_page_list.append(page)
            else:
                unique_page_list.append(page)
        return unique_page_list, duplicate_page_list

    @staticmethod
    def sort_page_list(page_list):
        for page in page_list:
            page.house_list.sort(key=lambda h: h.input_index)
        page_list.sort(key=lambda page: page.house_list[0].input_index)


def main(input_lines, page_size):
    # parse input lines as house entities
    house_info_dict = House.parse_input_as_houses(input_lines)
    total_house_count, house_count_list = House.sort_house_id_by_count(house_info_dict)
    # create an array of pages
    page_list = Page.create_page_list(page_size, total_house_count)
    duplicated_pageable_house_list = list([])
    # first_available_page_index
    page_index = 0
    for count, house_id in house_count_list:
        while page_list[page_index].is_page_full():
            page_index += 1
        # house list is created by the original input order
        house_list = house_info_dict[house_id]
        if Page.is_unique_pageable(count, page_list, page_index):
            Page.assign_house_to_pages_vertically(house_list, page_list, page_index)
        else:
            duplicated_pageable_house_list.extend(house_list)
    # now we have all duplicated houses that not uniquely pageable
    # first sort them by input index then assign them to the remained pages
    duplicated_pageable_house_list.sort()
    Page.assign_house_to_pages_sequentially(duplicated_pageable_house_list, page_list, page_index)
    # then split the page list into two page lists: one with no duplicate houses one with duplicated houses
    if page_size == 1:
        Page.sort_page_list(page_list)
        Page.print_pages(page_list)
        return
    last_page = page_list.pop()
    unique_page_list, duplicate_page_list = Page.split_pages(page_list)
    Page.sort_page_list(duplicate_page_list)
    Page.sort_page_list(unique_page_list)
    Page.print_pages(unique_page_list)
    Page.print_pages(duplicate_page_list)
    Page.print_pages([last_page])
    # then sort all pages with no duplicated houses by their first house's input index
    # finally, sort all houses in each page by their own input index then print the page


lines = """1,28,310.6,SF 
4,5,204.1,SF 
20,7,203.2,Oakland 
6,8,202.2,SF 
6,10,199.1,SF 
1,16,190.4,SF 
6,29,185.2,SF 
7,20,180.1,SF
7,22,80,SF
7,21,1,SF
6,29,9,SF""".split("\n")


for i in xrange(2, len(lines)+1):
    print "===============", i
    main(lines, i)
