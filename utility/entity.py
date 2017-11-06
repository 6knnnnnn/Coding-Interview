# -*- coding: utf-8 -*-


class TreeNode(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "{} (left={} right={})".format(self.val, self.left, self.right)


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        return "%s->%s" % (self.val, self.next)

    @staticmethod
    def array_to_nodes(array):
        head = ListNode(0)
        temp = head
        for a in array:
            temp.next = ListNode(a)
            temp = temp.next
        return head.next


class RandomListNode(object):
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None


class Interval(object):
    # 一般都需要将区间按照start从小到大排序，很少会按照end排序
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
    def get_end_key(interval):
        return interval.end


class UndirectedGraphNode:
    def __init__(self, x):
        self.label = x
        self.neighbors = []


"""
This is the interface that allows for creating nested lists.
You should not implement it, or speculate about its implementation
"""


class NestedInteger(object):
   def __init__(self, value=None):
       """
       If value is not specified, initializes an empty list.
       Otherwise initializes a single integer equal to value.
       """
       self.value = value
       self.child_list = list([])

   def isInteger(self):
       """
       @return True if this NestedInteger holds a single integer, rather than a nested list.
       :rtype bool
       """
       return self.value is not None

   def add(self, elem):
       """
       Set this NestedInteger to hold a nested list and adds a nested integer elem to it.
       :rtype void
       """
       self.child_list.append(elem)

   def setInteger(self, value):
       """
       Set this NestedInteger to hold a single integer equal to value.
       :rtype void
       """
       self.value = value

   def getInteger(self):
       """
       @return the single integer that this NestedInteger holds, if it holds a single integer
       Return None if this NestedInteger holds a nested list
       :rtype int
       """
       return self.value

   def getList(self):
       """
       @return the nested list that this NestedInteger holds, if it holds a nested list
       Return None if this NestedInteger holds a single integer
       :rtype List[NestedInteger]
       """
       return self.child_list

   def __repr__(self):
      res = ""
      if self.isInteger():
          res += "Int " + str(self.value)
      else:
          res += "List "
          for obj in self.child_list:
              res += str(obj) + "\n"
          res += "\n"
      return res
