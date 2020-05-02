# -*- coding: utf-8 -*-
"""

给定一个URL，里面可能有数字或者大小写字母，大小写需要区分，不同的组合可能合法也可能不合法

合法与否根据外围的一个API来判断，如果把某个URL的组合调用API返回的不是none，或者异常，则代表合法

给定一个URL，里面都是小写或者数字，判断在改变完了大小写后，哪些组合是合法的，哪些不是合法的。
"""

valid_pool = set([
    "123abcd", "123aBCD", "123abCD", "123ABcd"
])


def api_call(url_input):
    return url_input in valid_pool


def find_valid(raw_url):
    def dfs(raw_url, curr_url, start, global_res):
        if start == len(raw_url):
            if api_call(curr_url):
                global_res.append(curr_url)
            return
        c = raw_url[start]
        start += 1
        if c in "0123456789":
            # c is a number, no change to it, add to curr_url
            dfs(raw_url, curr_url + c, start, global_res)
        else:
            upper = curr_url + c.upper()
            dfs(raw_url, upper, start, global_res)
            lower = curr_url + c.lower()
            dfs(raw_url, lower, start, global_res)

    global_res = list([])
    if raw_url:
        dfs(raw_url, "", 0, global_res)
    return global_res


print find_valid("123ABCD")
