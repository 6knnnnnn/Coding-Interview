# -*- coding: utf-8 -*-


def read4(buf_list):
    # 给定一个buffer list，从文件中读取4个字符到这个buffer中（如果有的话）
    # 返回的是读进来的字符数，所以值域是[0, 4]，inplace改变了buffer list
    return len(buf_list)


def read(buf, n):
    # https://leetcode.com/problems/read-n-characters-given-read4
    # 想要读进来n个，返回的是最后实际读取了多少个字符，可能不到n
    # buf: 目标 buffer list (List[str])，把字符读进去
    i = 0  # 目前读取的总字符串数量
    while i < n:
        temp_buff = ['', '', '', ''] # 每次都是临时的
        count = read4(temp_buff) # 得到每次读取的数量
        if not count:
            break  # EOF 没有字符可以读了
        # n-i = how many remaining? 可能存在读了3个但是只需要2个的情况，找最小
        count = min(count, n - i)
        # 把临时buffer的内容copy到目标buf里面，此时只copy前count个，因为可能多读了
        buf[i:] = temp_buff[:count]
        i += count
    return i


class ReadMultipleTime(object):
    # https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times
    # 需要把多读的数据存到临时的queue里面，下次再次读取的时候先去queue里面找
    # 如果queue为空了，继续调用read4 API
    # 队列先进先出可以保持顺序不变，为空时就进队(read4)，不为空时就出队,并把出队的元素放到目标中
    def __init__(self):
        from collections import deque
        self.queue = deque([])

    def read(self, buf, n):
        # 仍旧返回最后读取了多少个字符
        total = 0
        temp_buf = [''] * 4
        while total < n:
            if not self.queue:
                # 历史不存在，调用read4 API
                num = read4(temp_buf)
                self.queue.extend(temp_buf[0:num])
            if not self.queue:
                break # 如果还是没有历史，此时说明文件没有东西可以读了
            if self.queue: # 有历史了，先从历史里面找
                buf[total] = self.queue.popleft()
                total += 1 # 直到 total == n，如果有的话
        return total
