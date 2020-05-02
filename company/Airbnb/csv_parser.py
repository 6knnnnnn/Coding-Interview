# -*- coding: utf-8 -*-
"""
可能需要提高的地方：

1. validate input format，很多edge case，比如 "Seattle, WA，即找不到匹配的double quote
2. 必要的时候raise exception：next item可能不存在，即i+1越界；或者出现mismatch的情况
3. 如果一个field里面有多个comma，比如"Seattle, WA, 12345, US"，此时需要找到下一个最后一个char是"的item，即用一个while循环
"""


def parse_line2(line):
    items = line.split(",")
    fields = list([])
    i = 0
    while i < len(items):
        item = str(items[i])
        # an empty string, or a paired double quotes, will be an empty field
        field = ''
        if len(item) != 0 and item != '""':
            field = item
            if item[0] == '"':
                if item[-1] != '"':
                    field = item[1:]
                    # 如果一个field里面有多个comma，比如"Seattle, WA, 12345, US"，此时需要循环找到下一个最后一个char是"的item
                    while i < len(items)-1 and items[i+1][-1] != '"':
                        i += 1
                        next_item = items[i]
                        field += "," + next_item
                        if next_item[0] == '"':
                            raise Exception
                    if field[-1] == '"':
                        field = field[:-1]
                    else:
                        # 此事说明field最后一个char不是"，然而item[0]="，所以我们有了mismatch
                        raise Exception
                else:
                    # a paired item between two double quotes "....."
                    # first replace "" to ", then remove the first and last double quote
                    field = item[1:-1].replace('""','"')
        fields.append(field)
        i += 1

    return "|".join(fields)


def parse_line(line):
    """
    刚开始的时候，用comma来分隔每一行，得到若干个items，之后开始parse each item，得到新的一行
    如果新的一个item为空（或者只有两个double quote），那么这一个field就是empty
    如果这个item第一个char不是double quote，item本身就是field，否则：
        判断item最后一个character是否为double quote
            如果是，即这是一个"...."，首尾都是double quotes，需要把他们截掉，以及把里面的""变为"（如果有的话）
            否则，需要找到下一个item，因为此时原始的输入是"... , ..."，那么item和next item分别对应","的左边和右边
                这里面假设不存在"... , ... , ..."的情况，即多个comma在两个double quote里面
                如果有的话，还需要继续寻找next item，直到next item[-1] == '"'
                这里假设next item[0] != '"'，否则就存在不合法的输入（比如 "Seattle, "WA"）
    """
    items = line.split(",")
    fields = list([])
    i = 0
    while i < len(items):
        item = str(items[i])
        # an empty string, or a paired double quotes, will be an empty field
        field = ''
        if len(item) != 0 and item != '""':
            field = item
            if item[0] == '"':
                # first char is double quotes, check two cases
                if item[-1] != '"':
                    # there is a ',' in the original field, need to get the next one
                    next_item = items[i+1]
                    if next_item[0] != '"' and next_item[-1] == '"':
                        # 第一个字符不是"，最后一个是"，so we have item = "Seattle  and next_item = WA"
                        field = item[1:]+","+next_item[:-1]
                        i += 1
                else:
                    # a paired item between two double quotes "....."
                    # first replace "" to ", then remove the first and last double quote
                    field = item[1:-1].replace('""','"')
        fields.append(field)
        i += 1

    return "|".join(fields)


inputs = [
'"John ""Brandon"" Smith",john.smith@gmail.com,"","Seattle, WA",  1',
'Jane Roberts,jane.roberts@gmail.com,"San Francisco, CA",2'
    ,'Alice Strong,alice_strong@aaa.com,"San Francisco, CA", 3'
]

for line in inputs:
    print line
    print parse_line(line)
    print "------"
