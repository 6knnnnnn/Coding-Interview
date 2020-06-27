class Node(object):
    def __init__(self, val, nextNode=None):
        self.val = val
        self.nextNode = nextNode

    def __repr__(self):
        return "{}->{}".format(self.val, self.nextNode)


def removeNodeGTX(head, x):
    if not head:
        return head
    if not head.nextNode:
        return None if head.val > x else head
    dummyHead = Node(0, head)
    p1, p2 = dummyHead, head
    while p2:
        # check p2
        while p2 and p2.val > x:
            p2 = p2.nextNode
        p1.nextNode = p2
        p1 = p2
        p2 = p2.nextNode if p2 else None

    return dummyHead.nextNode

def test1():
    n = head = Node(0)
    for i in [1, 2, 3, 5, 6, 7, 5, 4, 5]:
        n.nextNode = Node(i)
        n = n.nextNode
    head = head.nextNode
    print head
    print removeNodeGTX(head, 4)


def intersection_of_2_linked_list(headA, headB):
    """
    https://leetcode.com/problems/intersection-of-two-linked-lists
    len of nodes in A before the intersection: x
    len of nodes in B before the intersection: y
    len of nodes in the intersection, if any: z
    x + z = len(A), y + z = len(B), offset = abs(x-y)
    start from the longer one and reach to the node at offset, then use two pointers
    """
    def getSize(head):
        size = 0
        while head:
            size, head = size + 1, head.next
        return size

    l1, l2 = getSize(headA), getSize(headB)
    longer = headA if l1 > l2 else headB
    shorter = headA if l2 > l1 else headB
    offset = abs(l2-l1)
    while offset:
        longer, offset = longer.next, offset - 1
    while longer and shorter:
        if longer == shorter:
            return longer
        longer, shorter = longer.next, shorter.next
    return None
