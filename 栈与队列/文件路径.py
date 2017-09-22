# -*- coding: utf-8 -*-


class PathNode(object):
    def __init__(self, name, depth, length):
        self.name = name
        self.depth = depth
        self.length = length

    def is_file(self):
        return '.' in self.name


def length_longest_path(input_path):
    """
    https://leetcode.com/problems/longest-absolute-file-path/description/
    技巧一：用split(‘\n’) 将原串分割开，相当于一次读一行
    技巧二：利用’\t’的个数来当前目录/文件，在第几层
    技巧三：从上到下一行一行顺序读入，用类似栈操作，把前面几层的字符串长度都记下来(画图模拟)
    用Stack来表示每个path node
    """
    if not input_path:
        return 0
    maxlen = 0
    stack = list([])
    lines = str(input_path).splitlines()
    root_node = PathNode(lines[0], 0, len(lines[0]))
    if root_node.is_file():
        return root_node.length
    stack.append(root_node)
    for line in lines[1:]:
        path_name = line.lstrip("\t") # 去掉leading '\t'
        curr_depth = len(line) - len(path_name)
        # 确保当前path与stack顶端的path node是父子关系
        # 即是里面的文件或者文件夹，curr depth必须小于栈顶的depth
        while stack and stack[-1].depth >= curr_depth:
            stack.pop()
        if not stack:
            break # 必须stack非空
        prev_node = stack[-1]
        curr_node = PathNode(path_name, curr_depth, len(path_name)+prev_node.length+1)
        if curr_node.is_file():
            maxlen = max(curr_node.length, maxlen)
        else: # 把文件夹放到stack里面
            stack.append(curr_node)
    return maxlen


def test():
    test_path = [
        "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext",
        "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext",
        "root", # 单一文件夹
        "root.txt", # 单一文件
        "dir\n\tfile.txt",
        "dir\n\tdir2\tdir3" # 全是文件夹
        ]

    for test in test_path:
        print length_longest_path(test)


def simplify_path(path):
    """
    https://leetcode.com/problems/simplify-path/description/
    简化一个UNIX 系统文件夹路径，比如：
    path = "/home/", => "/home"
    path = "/a/./b/../../c/", => "/c"
    用Stack：先把input path按照'/'分割，之后遍历每个元素，如果是'.'，不变，如果是'..'，pop出栈顶
    其他情况（假设input path 格式是合法的），加入到stack中
    Edge case是，如果最后stack为空，也要输出'/'，即总目录
    """
    path_list, stack = path.split('/'), list([])
    for p in path_list:
        if p == '.' or p == '':
            continue
        elif p == '..':
            if len(stack) > 0:
                stack.pop()
        else:
            stack.append(p)
    return '/' + '/'.join(stack)
