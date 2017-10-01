# -*- coding: utf-8 -*-


def palindrome_linked_list(head):
    """
    https://leetcode.com/problems/palindrome-linked-list/description/
    判断一个链表是否是回文的。暴力解法直接用一个stack，然后一次比较stack中的值和head开始，是否相同。
    或者把list partition分成左右两部分（用快慢指针），然后逆序其中一个，然后比较左右两部分是否一样。
    """
    fast = slow = head
    # find the mid node
    while fast and fast.next:
        fast, slow = fast.next.next, slow.next
    # reverse the second half
    reverse_head = None
    while slow:
        nxt = slow.next
        slow.next = reverse_head
        reverse_head = slow
        slow = nxt
    # compare the first and second half nodes
    while reverse_head:  # while node and head:
        if reverse_head.val != head.val:
            return False
        reverse_head = reverse_head.next
        head = head.next
    return True


def palindrome_number(x):
    """
    https://leetcode.com/problems/palindrome-number/description/
    判断一个数字是否是回文，最简单的转换成string，但是需要额外空间，或者把数字逆序之后，判断是否跟输入一样。
    """
    # x= 10 * x / 10 + x % 10
    if x < 0:
        return False
    y = 0
    cp = x
    while x > 0:
        y = y * 10 + x % 10
        x = x / 10
    return cp == y


def palindrome_permutation(s):
    """
    https://leetcode.com/problems/palindrome-permutation/description/
    判断一个string是否能够组成回文排列，也就是根据字母的个数的奇偶性来判断
    """
    count_set = set([])
    for c in s:
        if c in count_set:
            count_set.remove(c)
        else:
            count_set.add(c)
    if len(s) % 2 == 0:
        # string的长度为偶数，判断每个字母的个数是否全都是偶数
        return len(count_set) == 0
    # 否则，string长度为奇数，判断是否只有一个字母的个数是奇数
    return len(count_set) == 1


def valid_palindrome(s):
    """
    https://leetcode.com/problems/valid-palindrome/description/
    判断一个string是否满足回文，可以忽略标点符号和空格。
    双指针，过滤掉不需要的字符，直到下一个有效char（可以是字母或者数字）。
    """
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True


def valid_palindrome_delete_1(s):
    """
    https://leetcode.com/problems/valid-palindrome-ii/description/
    给定一个string，最多删除一个字母的情况下，判断是否可以为回文。
    还是用two pointers，从左右两边开始比较。如果到最后left >= right，即所有的都match，说明不用delete已经是回文
    否则，对于第一次出现mismatch的点，即left和right，删除left然后判断下边的是否匹配，或者删除right继续判断。
    如果有一个结果为True，说明可以删除一个达到回文。否则返回False
    """
    def is_palindrome(s, i, j):
        while i < j:
            if s[i] == s[j]:
                i, j = i+1, j-1
            else:
                return False
        return True

    left, right = 0, len(s)-1
    while left < right and s[left] == s[right]:
        left, right = left + 1, right - 1
    if left >= right:
        # 此时说明，所有的都检查完了，string已经是匹配的了
        return True
    # 否则，删除left，匹配剩下的s[left+1:right]，或者删除right，匹配剩下的s[left:right-1]
    return is_palindrome(s, left+1, right) or is_palindrome(s, left, right-1)
