# -*- coding: utf-8 -*-

# Karatsuba algorithm

from Utility import ListNode


class AddLinkedList(object):

    @staticmethod
    def plus_one_linked_list_stack(head):
        # https://leetcode.com/problems/plus-one-linked-list/description/
        # head为最大位置的digit，以此类推，用stack，到最后一位时候，+1，如果carry为1，依次pop stack
        if not head:
            return
        stack = list([])
        new_head = ListNode(1)
        new_head.next = node = head
        while node:
            stack.append(node)
            node = node.next
        # 遍历到最后node
        carry = 1
        while stack:
            node = stack.pop()
            node.val += carry
            if node.val >= 10:
                node.val -= 10
            else:
                # 此时carry为0，且stack还有元素，即没有回到最开始的head，不需要用new head
                return head
        return new_head # 否则返回new head，初始化为1

    @staticmethod
    def plus_one_linked_list_recur(head):
        if not head:
            return ListNode(1)
        carry = AddLinkedList.plus_one_linked_list_recur(head.next)
        if carry != head.next:
            head.val += 1 # carry from next
        if head.val <= 9: # no carry needed
            return head
        head.val -= 10 # head.val == 10
        carry.next = head
        return carry

    @staticmethod
    def add_two_numbers_original_order_stack_way(l1, l2):
        # https://leetcode.com/problems/add-two-numbers-ii/description/
        # 如果是原始的顺序，可以用一个stack来逆序遍历；或者将两个输入逆序，相加后再逆序回来
        s1, s2, s3 = list([]), list([]), list([])
        while l1:
            s1.append(l1.val)
            l1 = l1.next
        while l2:
            s2.append(l2.val)
            l2 = l2.next
        c = 0
        while c > 0 or len(s1) > 0 or len(s2) > 0:
            val = c
            val += s1.pop() if len(s1) > 0 else 0
            val += s2.pop() if len(s2) > 0 else 0
            c = 1 if val >= 10 else 0
            val -= 10 if val >= 10 else 0
            s3.append(val)
        temp = head = ListNode(0)  # place holder
        while s3:
            # 逆序遍历stack
            temp.next = ListNode(s3.pop())
            temp = temp.next
        return head.next

    @staticmethod
    def add_two_numbers_original_order_recursion(l1, l2):
        def get_len(head):
            count = 0
            while head:
                count += 1
                head = head.next
            return count

        def recursion(longer, shorter, offset):
            # 如果知道了两个list的长度，找到较长的和较短的，以及两者的差值offset，根据offset判断之后递归的状态
            if not longer:
                return None
            # offset=0，说明两者当前节点长度一样，也就是数位一样，需要相加
            current = ListNode(longer.val if offset else longer.val + shorter.val)
            # post就是当前节点的所有后面的节点的相加结果，因为offset=0，仅说明两者后边的长度相等，但可能还有节点
            # offset不为0，说明longer比shorter还是要长，用longer下一个和shorter继续相加
            post = recursion(longer.next, shorter, offset-1) if offset else recursion(longer.next, shorter.next, 0)
            if post and post.val >= 10:
                # 改变carry，即当前节点的value
                current.val += 1
                post.val -= 10
            current.next = post
            return current

        len1, len2 = get_len(l1), get_len(l2)
        new_head = ListNode(0)
        longer = l1 if len1 > len2 else l2
        shorter = l2 if len1 > len2 else l1
        new_head.next = recursion(longer, shorter, abs(len1 - len2))
        if new_head.next and new_head.next.val >= 10:
            # 如果new head之后的值大于10，carry=1加到当前new head，此时new head就是结果，否则是new head得下一个
            new_head.next.val -= 10
            new_head.val += 1
            return new_head
        return new_head.next

    @staticmethod
    def add_two_numbers_reverse_order(l1, l2):
        # https://leetcode.com/problems/add-two-numbers/description/
        # test case: a = 1->8->6, b = 1->2->3, result=2->0->0->1
        current = new_head = ListNode(0)
        carry = 0
        while l1 or l2 or carry:
            if l1:
                carry += l1.val
                l1 = l1.next
            if l2:
                carry += l2.val
                l2 = l2.next
            current.val += carry
            carry = 0
            if current.val >= 10:
                current.val -= 10
                carry = 1 # 下次的carry为1
            if l1 or l2 or carry:
                # 如果还有继续的必要，current挪到下一个
                current.next = ListNode(0)
                current = current.next
        return new_head


def add_two_strings(num1, num2):
    """
    https://leetcode.com/problems/add-strings/description/
    输入都是正序表达的数字，比如'123'+'1'='124'。
    因为ord('0') = 48, 所以对于任意char c, ord(c)-48就是c对应的int
    """
    reverse_list = list([])
    i, j = len(num1)-1, len(num2)-1
    carry = 0
    while i >= 0 or j >= 0 or carry:
        n1 = ord(num1[i]) - 48 if i >= 0 else 0
        n2 = ord(num2[j]) - 48 if j >= 0 else 0
        value = n1 + n2 + carry
        carry = 0
        if value >= 10:
            value = value - 10
            carry = 1
        reverse_list.append(str(value))
        i, j = i-1, j-1
    return ''.join(reverse_list[::-1])


def add_binary(a, b):
    if not a or len(a) == 0:
        return b
    if not b or len(b) == 0:
        return a
    i, j, carry = len(a)-1, len(b)-1, 0
    res = list([]) # 可能需要第一位是carry
    while carry or i >=0 or j >= 0:
        carry += 1 if i >= 0 and a[i] != '0' else 0
        carry += 1 if j >= 0 and b[j] != '0' else 0
        if carry <= 1:
            res.append(str(carry))
            carry = 0
        elif carry == 2:
            res.append('0')
            carry = 1
        elif carry == 3:
            res.append('1')
            carry = 1
        i, j = i - 1, j - 1
    return "".join(res[::-1])

test = [["100","1"], ["1","1"], ["0", "111"], ["111", "1"], ["111", "1111"]]

for t in test:
    print t[0], t[1], add_binary(t[0], t[1])