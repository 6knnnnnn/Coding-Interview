# -*- coding: utf-8 -*-


class FunctionNode(object):
    def __init__(self, function_id, start_time):
        self.function_id = function_id
        self.start_time = int(start_time)
        self.exclusive_time = self.end_time = 0

    def get_execution_time(self):
        # 每次一个函数出栈，计算出执行时间 = end - start - exclusive + 1
        return self.end_time - self.start_time - self.exclusive_time + 1

    def end(self, end_time):
        self.end_time = int(end_time)

    def add_exclusive_time(self, exclusive_time):
        self.exclusive_time += int(exclusive_time)

    def __repr__(self):
        return "%s:%s:%s:%s" % (self.function_id, self.end_time, self.start_time, self.exclusive_time)


def exclusive_function_time(n, logs):
    """
    https://leetcode.com/problems/exclusive-time-of-functions/description/
    假设已知有n个函数，logs里面是函数的执行情况，里面有很多行，每行的格式：function_id:start or end:timestamp
    timestamp是用int表示，并且是排好序的。函数A有可能调用函数B，所以这里计算函数A的执行时间的时候，需要排除掉函数B的执行时间
    假设所有函数都会end，而且可能递归调用（即同一个函数执行多次），要求输出最后n个函数的总执行时间。
    Input: n = 2 logs =
    ["0:start:0",
    "1:start:2",
    "1:end:5",
    "0:end:6"]  Output:[3, 4]
    解法：用一个stack模拟，每个元素代表的是 function ID, start time, end time, exclusive time（需要排除其他函数的时间）
    每当有一个新的function start，加入到stack；每当有一个function end，根据end time算出对应的execution time更新结果
    关键点：1）如果有recursive call，此时因为是同一个function id，所以不用入stack，只需要更新stack top即可
           2）如果不是recursive call，该函数结束，即出栈的时候，算出来自己的执行时间a，并把a更新为调用函数的exclusive time
           3）每次一个函数出栈，计算出执行时间 = end - start - exclusive + 1，更新function id对应的array数值
    Follow up: 遇到recursive call，需要合并以节省空间？
        在FunctionNode当中需要一个count来记录recursive call的个数。每次也是跟top比较，如果function id一样，而且count>0，
        此时说明当前的function是之前的同一个function的recursive call，此时需要"合并"，即更新end time
        此外还需要更新count -= 1，如果count = 0了，出栈（recursive call结束），更新execution time
    """
    # 初始化结果数组，含有n个元素，index就是对应的function id
    results = [0] * n
    stack = list([])
    for log in logs:
        function_id, status, timestamp = log.split(':')
        if status == 'start':
            stack.append(FunctionNode(function_id, timestamp))
        elif status == 'end':
            # 这里假设stack非空，而且top node的function id 和 当前function id相同，否则需要处理异常
            top_function = stack.pop()
            top_function.end(timestamp)
            execution_time = top_function.get_execution_time()
            results[int(function_id)] += execution_time
            if stack:
                # 如果还有function没执行完的话，更新top，也就是调用当前function的函数
                # 需要把当前函数的执行时间以及exclusive time，加入到调用函数的exclusive time里面
                stack[-1].add_exclusive_time(top_function.exclusive_time + execution_time)
    return results


def tests():
    logs = [
        ["0:start:0", "0:start:1", "0:start:2", "0:end:3", "0:end:4", "0:end:5"],
        ["0:start:0", "0:end:10"], # 只有自己
        ["0:start:0", "0:end:10", "0:start:11", "0:end:20"], # 只有自己，非recursive
        ["0:start:0", "0:start:10", "0:end:11", "0:end:20"],  # 只有自己，recursive
        ["0:start:0", "0:start:10", "1:start:20", "1:end:25", "0:end:31", "0:end:40"], # 多个，没有互相调用
        ["0:start:0", "1:start:2", "1:end:5", "0:end:6"], # 多个，调用了别的
        ["0:start:0", "1:start:2", "1:end:5", "1:start:7", "1:end:10", "0:end:16"], # 多个，有recursive
        ["0:start:0", "1:start:2", "1:end:5", "1:start:7", "0:start:8", "0:end:9", "1:end:10", "0:end:16"],
        # 多个，有recursive，而且是互相调用
    ]
    for log in logs:
        n = len(log) / 2
        print exclusive_function_time(n, log)

tests()
