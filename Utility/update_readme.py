# -*- coding: utf-8 -*-
import os

leet_code_url = "https://leetcode.com/problems"
same_problem_series = "iiiv"
leetcode_source_str_newline = "\n\t"


class CodingProblemEntity(object):
    def __init__(self, problem_name, problem_source, solution_location):
        self.problem_name = problem_name
        # 可能有多个source，或者同一个题目的不同变体问题i ii iii iv等等
        self.problem_source_list = list([problem_source])
        self.solution_location = solution_location

    def __repr__(self):
        problem_source_list = sorted(self.problem_source_list)
        problem_source_list_str = leetcode_source_str_newline.join(problem_source_list)
        return "%s:\n%s\n%s" % (self.problem_name, self.solution_location, problem_source_list_str)

    def add_new_source(self, problem_source):
        self.problem_source_list.append(problem_source)


def list_all_files(working_dir):
    py_files_list = list([])
    for path, _, files in os.walk(working_dir):
        for name in files:
            if name.endswith(".py"):
                py_files_list.append(os.path.join(path, name))
    return py_files_list


def read_content_from_file(file_path):
    content = ""
    if os.path.exists(file_path.strip()):
        with open(file_path, 'r') as f:
            content = f.read()
            f.close()
    return content


def parse_file_content(file_path, content):
    lines = content.split("\n")
    i = 0
    global_problem_entity_dict = dict([])
    while i < len(lines):
        # First find the def part
        line = lines[i].strip()
        i += 1
        if line.find("def") == 0:
            # find a new one
            while i < len(lines):
                problem_leetcode_source = lines[i].strip()
                i += 1
                if problem_leetcode_source.find(leet_code_url) >= 0:
                    # 找到一个新的CodingProblemEntity
                    problem_name = problem_leetcode_source[len(leet_code_url):]
                    if problem_leetcode_source.find("/description") > 0:
                        description_index = problem_leetcode_source.find("/description")
                        problem_name = problem_leetcode_source[:description_index]
                    problem_name_list = problem_name.split("-")
                    problem_full_name = ""
                    if problem_name_list[-1] in same_problem_series:
                        # 如果是变体题目，理论上应该都在一个文件夹内，此时problem_full_name需要删掉最后的题号
                        problem_name_list.pop()
                    for word in problem_name_list:
                        problem_full_name += "%s%s" % (word[0].upper(), word[1:])
                    if problem_full_name not in global_problem_entity_dict:
                        problem_entity = CodingProblemEntity(problem_full_name, problem_leetcode_source, file_path)
                        global_problem_entity_dict[problem_full_name] = problem_entity
                    else:
                        global_problem_entity_dict[problem_full_name].add_new_source(problem_leetcode_source)
    return global_problem_entity_dict


def write_to_read_me(readme_file_path):
    with open(readme_file_path, 'w') as readme_file:
