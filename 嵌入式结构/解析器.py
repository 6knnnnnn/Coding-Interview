# -*- coding: utf-8 -*-
from utility.entity import NestedInteger


def mini_parser(s):
    """
    http://www.cnblogs.com/grandyang/p/5771434.html

    https://leetcode.com/problems/mini-parser/description/
    给定一个string，里面包含了数字0-9，方括号[ ]，逗号，以及-负号
    要求parse出来一个NestedInteger object，这个object可能会有integer或者list

    用一个stack存放对应的NestedInteger object，首先按照comma分割之后，遍历每个元素，分情况讨论：
    1）第一个是[：    [123   [123]    [123]]... 或者 ...[[123
    此时需要创建一个list object，之后再根据num创建一个integer object 加入到这个list，然后把这个list加入到stack
    2）第一个不是[：  -123    123]     123]]...
    此时需要创建一个integer object，加入到stack top即可

    如果最后有]，说明stack需要pop top，pop的次数等于]的个数
    每次pop出来的obj，说明此时已经完结了，需要加到他的上一级，也就是pop之后stack new top
    """
    root = None
    stack = list([])
    if s:
        item_list = s.split(",")
        if len(item_list) == 1 and '[' not in s and ']' not in s:
            # 只有一个元素，且不是list，而是单纯的integer
            return NestedInteger(value=int(s))
        for item in item_list:
            item_list = list(item[1:]) if item[0] == '[' else list(item)
            pop_count = 0
            while item_list and item_list[-1] == ']':
                # 需要根据pop_count来判断有多少个nested obj需要从stack里面pop出来，即根据]的个数
                item_list.pop()
                pop_count += 1
            num = None
            # 此时item list里面可能为空需要检查，比如item = "[]"的情况，那么num实际上是None而非int
            if item_list:
                num = int(''.join(item_list))
            integer_obj = NestedInteger(num)
            if item[0] == "[":
                # 此时需要创建一个nested list object
                list_obj = NestedInteger()
                list_obj.add(integer_obj)
                stack.append(list_obj)
            else:
                # 此时如果输入合法，stack肯定不为空
                stack[-1].add(integer_obj)
            # poll stack if any ] in item tail
            while pop_count > 0 and stack:
                pop_count -= 1
                # 最后如果stack里面只有一个元素了，那么就是最后的pop出来的root了
                root = stack.pop()
                if stack:
                    stack[-1].add(root)
    return root


samples = [#"[1, 2]",
           "[1,[4,[7]],0]", "123", "[123]", "[[123]]"]

for s in samples:
    print mini_parser(s)


