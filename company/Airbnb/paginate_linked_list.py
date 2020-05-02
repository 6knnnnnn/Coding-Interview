
class House(object):
    # A house entity node used in a doubly linked list
    def __init__(self, house_id, list_id, points, city, input_index):
        self.house_id = house_id
        self.list_id = list_id
        self.points = float(points)
        self.city = city
        self.prev = self.next = None
        # input index is used for debug purposes
        self.input_index = input_index

    def __str__(self):
        return "%s,%s,%s,%s" % (self.house_id, self.list_id, self.points, self.city)

    def __repr__(self):
        # used for debug purposes
        return "%s %s" % (self.input_index, self.house_id)

    def de_link(self):
        # Remove current house node from linked list, and return its next element
        if self.next:
            self.next.prev = self.prev
        if self.prev:
            self.prev.next = self.next
        return self.next

    @staticmethod
    def parse_input_as_houses(lines):
        # house_head is the placeholder of the doubly linked list by parsing from input lines
        house = house_head = House(-1, -1, -1, -1, -1)
        house_total_count = 0
        for i, line in enumerate(lines):
            data = line.strip().split(",")
            if data and len(data) >= 4:
                house.next = House(data[0], data[1], data[2], data[3], house_total_count)
                house.next.prev = house
                house = house.next
                house_total_count += 1
        return house_head


def main(input_lines, page_size):
    house_head = House.parse_input_as_houses(input_lines)
    page_list = list([])
    while house_head.next:
        # process all house nodes after house_head, i.e. from house_head.start
        curr_house = house_head.next
        page_list.append([])
        curr_page = page_list[-1]
        curr_page_house_id_set = set([])
        while curr_house and len(curr_page) < page_size:
            # process the current page
            if curr_house.house_id not in curr_page_house_id_set:
                # first time, not duplicated
                curr_page.add(str(curr_house))
                curr_page_house_id_set.add(curr_house.house_id)
                # remove current house from the linked list, and continue to its next
                curr_house = curr_house.de_link()
            else:
                # duplicated, move to next
                curr_house = curr_house.next
        if len(curr_page) < page_size:
            # current page not full yet, we cannot find unique house for this page anymore
            # then we start over from the head to get any house node (if any, as last page doesn't have to be full)
            curr_house = house_head.next
            while curr_house and len(curr_page) < page_size:
                curr_page.add(str(curr_house))
                curr_house = curr_house.de_link()
    for page in page_list:
        for curr_house in page:
            print curr_house
        print ""
    return page_list


def test1():
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

    total = len(lines)+1
    for i in xrange(1, total):
        print "===============", i
        main(lines, i)


def test2():
    lines = """
    1,28,310.6,SF 
    4,5,204.1,SF
    20,7,203.2,Oakland
    6,8,202.2,SF 
    6,10,199.1,SF
    1,16,190.4,SF
    6,29,185.2,SF 
    7,20,180.1,SF 
    6,21,162.1,SF
    2,18,161.2,SF 
    2,30,149.1,SF
    3,76,146.2,SF
    2,14,141.1,San Jose
    """.split("\n")
    main(lines, 5)

test1()
