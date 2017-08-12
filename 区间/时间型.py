class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return "({}, {})".format(self.start, self.end)

    @staticmethod
    def list_to_interval(input_list):
        interval_list = list([])
        for input in input_list:
            interval_list.append(Interval(input[0], input[1]))
        return interval_list

    @staticmethod
    def get_start_key(interval):
        return interval.start

    @staticmethod
    def has_interval_overlap(interval_list):
        sorted(interval_list, key=Interval.get_start_key)
        for i in xrange(1, len(interval_list)):
            prev, curr = interval_list[i-1], interval_list[i]
            if prev.start > curr.end:
                return True
        return False

    @staticmethod
    def min_spaces_required(interval_list):
        start, end = list([]), list([])
        for i in interval_list:
            start.append(i.start)
            end.append(i.end)
        start.sort(); end.sort()
        available = total = i = j = 0
        while i < len(start):
            if start[i] < end[j]:
                if available > 0:
                    available -= 1
                else:
                    total += 1
                i += 1
            else: # no overlap
                available += 1
                j += 1
        return total

    @staticmethod
    def merge_intervals(interval_list):
        pass

    @staticmethod
    def insert_interval(interval_list, targer):
        pass


sample = [[1,2], [2,5], [4,5]]

interval_list = Interval.list_to_interval(sample)

print Interval.min_spaces_required(interval_list)