

def swapPairs(head):
    # https://leetcode.com/problems/swap-nodes-in-pairs/
    if not head or not head.next:
        return head
    # more than 2 nodes
    p1, p2, p3 = head, head.next, head.next.next

    p2.next = p1
    p1.next = swapPairs(p3)
    return p2


def reverseNodesKGroup(head, k):
    # https://leetcode.com/problems/reverse-nodes-in-k-group/
    def reverse(head):
        # more than two nodes
        p1, p2 = head, head.next
        p1.next = None
        while p2:
            p3 = p2.next
            p2.next = p1
            p1, p2 = p2, p3
        return p1
    if not head or not head.next:
        return head
    # first find k nodes, then reverse them, assuming more than one node
    p, i = head, 1
    while p.next and i < k:
        p, i = p.next, i + 1
    if i == k:
        # find k nodes
        afterKHead, p.next = p.next, None
        newHead = reverse(head)
        # original head is now the tail of new head
        head.next = reverseNodesKGroup(afterKHead, k)
        return newHead
        # less than k nodes
    return head


from utility.entity import ListNode
for k in [2, 3, 5]:
    head = ListNode.array_to_nodes([1,2,3,4,5,6,7])
    print k, reverseNodesKGroup(head, k)

for k in [3]:
    head = ListNode.array_to_nodes([1,2,3,4,5])
    print k, reverseNodesKGroup(head, k)
