# -*- coding: utf-8 -*-


def minimum_window_substring(A, B):
    """
    字符串A与B，找到A中包含所有B的字符串的最小substring
    把问题转换理解为，A需要按照顺序从自己的字符串中，抠出来还给B，也就是A owe B 的字符串
    当A中的某个window包含了B中所有的字符时，window为目标substring，但问题是如果有冗余怎么更新窗口？
    1. 首先词频map，初始化为所有B的字符的词频，A所欠B的总数total初始为B的唯一的字符长度
    2. 之后遍历A，更新window、map和total：
        1)  先是right向右移动，每次遇见一个新的A[right]，如果这个字符存在于B中，在词频map中-1。如果更新后为0
            此时代表A对于该字符已经不欠B了，此时更新total-1，即A少欠B了一种字符（一种不是一个）
        2)  当total为0时，此时词频map中所有value均<=0，表明A还完了B，而且还有多还的冗余的（为负值的），right停止移动
        3)  开始移动left，A[left]从窗口中滑出去"之前"，如果该字符存在于B，将这个马上就滑出去的字符在词频map中的值+1
        4)  如果A[left]词频map中值>0，表明如果滑出去left，A将要重新开始欠B
        5)  此时，[left, right] 是一个目标window，但不一定是全局最小
            需要根据之前记录的最小window 长度来判断，如果是更小的，记录left为开始位置，并更新min len
    3. 之后再从这个window的right index开始滑动，即从新创建一个window，total重置为B的长度，词频map重置
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