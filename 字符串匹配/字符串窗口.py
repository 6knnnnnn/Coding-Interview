# -*- coding: utf-8 -*-


def minimum_window_substring(A, B):
    """
    https://leetcode.com/problems/minimum-window-substring/description/
    字符串A与B，A比B长，找到A中包含所有B的字符串的最小substring
    把问题转换理解为，A需要按照顺序从自己的字符串中，抠出来还给B，也就是A owe B 的字符串，解法：词频统计+双指针
    当A中的某个window包含了B中所有的字符时，window为目标substring，但问题是如果有冗余怎么更新窗口？
    1. 首先词频map，初始化为所有B的字符的词频，A所欠B的总数total初始为B的唯一的字符长度
    2. 之后遍历A，更新window、map和total：
        1)  先是right向右移动，每次遇见一个新的A[right]，如果这个字符存在于B中，在词频map中-1。如果更新后为0
            此时代表A对于该字符已经不欠B了，此时更新total-1，即A少欠B了一种字符（一种，不是一个）
        2)  当total为0时，此时词频map中所有value均<=0，表明A还完了B，而且还有多还的冗余的（为负值的），right停止移动
        3)  开始移动left，A[left]从窗口中滑出去"之前"，如果该字符存在于B，将这个马上就滑出去的字符在词频map中的值+1
        4)  如果A[left]词频map中值>0，表明如果滑出去left，A将要重新开始欠B
        5)  此时，[left, right] 是一个目标window，但不一定是全局最小
            需要根据之前记录的最小window 长度来判断，如果是更小的，记录left为开始位置，并更新min len
    3. 之后再从这个window的right index开始滑动，即从新创建一个window，total重置为B的长度，词频map重置
    4. 如果最后需要返回的是A中的最短substring，那么需要记录min window starting index，再加上min len，就是目标结果
    """
    d = {}
    left = right = min_win_i = 0
    for c in B:
        d[c] = d.get(c, 0) + 1
    owe_total, min_len = len(d), len(A) + 1
    while right < len(A):
        c_right = A[right]
        right += 1
        if c_right in d:
            d[c_right] -= 1 # 如果为负数，表明目前的窗口里面有冗余的存在于B的字符c_right
            if d[c_right] == 0: # 仅在为0的时候更新owe total
                owe_total -= 1
        # owe total == 0 表明找到了一个新的窗口
        while owe_total == 0:
            c_left = A[left]
            if c_left in d:
                d[c_left] += 1
                if d[c_left] > 0:
                    # 因为此时A第一次重新开始欠B，[left, right] 就是一个目标substring
                    owe_total += 1
                    curr_window_len = right - left
                    if curr_window_len < min_len:  # update min_win_i
                        min_len = curr_window_len
                        min_win_i = left
            left += 1
    return A[min_win_i:min_win_i + min_len] if min_len != len(A) + 1 else ""


print minimum_window_substring("aaiibcdabjc", "abc")


# Anagrams 元素出现次数一样，而且排序后也一定一样


def valid_anagram(s1, s2):
    # hash map O(N) 时间+空间
    # 排序，O(NlogN) 时间，O(N)空间（string immutable除非是char array）
    return sorted(s1) == sorted(s2)


# Given an array of strings, group anagrams together.
# https://leetcode.com/problems/group-anagrams
def group_anagrams_sort(str_list):
    # 排序后分组，O(N * M * logM)，M平均长度，N单词个数
    d = {}
    for s in str_list:
        sort = "".join(sorted(s))
        if sort in d:
            d[sort].add(s)
        else:
            d[sort] = list([s])
    return d.values()


def group_anagrams_prime(str_list):
    # 26个字母，每一个安排一个prime numbers，不同字母组合的乘积，肯定不一样
    # 所以算出所有str的素数乘积，乘积相等的就是anagrams，时间O(M * N)
    # 可能的问题是，单词过长，导致乘积过大，overflow
    primes = [2, 3, 5, 7, 11 ,13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107]
    ana_map = dict([])
    for s in str_list:
        product = 1
        for c in s:
            product *= primes[ord(c)-97]
        if product not in ana_map:
            ana_map[product] = list([])
        ana_map[product].add(s)
    return ana_map.values()


def test_group():
    str_list = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print group_anagrams_prime(str_list)
    print group_anagrams_sort(str_list)


class AnagramsWindow(object):
    def __init__(self, target):
        from collections import deque
        self.queue = deque([])
        self.target = {} # 需要比较的目标
        self.current = {} # 当前window所包含的char count map
        for c in target:
            self.target[c] = self.target.get(c, 0)+1 # letter count
            self.current[c] = 0 # 初始化均为0
        self.total = len(target)
        # 这里的距离衡量的依据是，有几个char的数量是不等的，所以最多为keys的数量
        # 这一点和min substring window的概念有点像，都是找两个string之间的distance
        self.distance = self.distinct_keys = len(self.current.keys())

    def handle_change(self, c, is_remove):
        """
        如果c不在target中，删除或者新增c都不会改变距离，否则：
        删除c会把current map里面的count-1，反之新增会+1
        两种情况，都需要最后根据c在current和target中的count，来更新current与target的距离
        也就是当current[c] == target[c], distance需要-1，否则+1，但distance有上限
        """
        if c is not None and c in self.target:
            self.current[c] += -1 if is_remove else 1
            if self.current[c] == self.target[c]:
                self.distance -= 1
            else:
                # 距离最多为target中唯一char的数量
                self.distance = min(self.distinct_keys, self.distance + 1)

    def slide_right(self, new):
        self.queue.append(new)
        left = self.queue.popleft() if len(self.queue) == self.total+1 else None
        if left != new:
            # 相同则不需要改变，避免重复字符的情况，比如aaaa...a里面找aaa
            self.handle_change(left, True)
            self.handle_change(new, False)

    def is_anagram(self):
        return len(self.queue) == self.total and self.distance == 0


def substring_anagrams(s, p):
    # https://leetcode.com/problems/find-all-anagrams-in-a-string/description/
    # Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.
    # 可以用暴力解法，但如果输入是：aaaa....a, p=aaa，那么会很费时，O(M * N)
    # O(N)解法，滑动窗口找距离，空间O(M)，时间O(N)
    res = []
    window = AnagramsWindow(p)
    for i, c in enumerate(s):
        window.slide_right(c)
        if window.is_anagram():
            res.append(i-len(p)+1) # 新加的是开始的index
    return res


test_list = [ ["abaacbabc", "abc"]
             ,["abcdebcafg", "abc"]
             ,["abab", "ab"]
             ,["aaaaaaaaa", "a"]
             ,["aaaaaaaaa", "aaa"]
             ,["aaaaaaaaa", "abc"]]

for test in test_list:
    print test, substring_anagrams(test[0], test[1])