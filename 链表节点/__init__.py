
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
