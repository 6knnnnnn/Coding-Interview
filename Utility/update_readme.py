# -*- coding: utf-8 -*-
import os

leet_code_url = "https://leetcode.com/problems"
same_problem_series = "iiiv"


class CodingProblemEntity(object):
    def __init__(self, solution_location):
        # 可能有多个source，或者同一个题目的不同变体问题i ii iii iv等等
        self.problem_name_set = set([])
        self.solution_location = solution_location
        if solution_location.endswith('.py'):
            self.solution_location = solution_location[0:-3]

    def __repr__(self):
        problem_name_list = sorted(list(self.problem_name_set))
        problem_name_list_str = "\n\t".join(problem_name_list)
        return "###### %s\n\t%s" % (self.solution_location, problem_name_list_str)

    def add_new_problem(self, problem_name):
        self.problem_name_set.add(problem_name)


def list_all_files(working_dir):
    py_files_list = list([])
    for path, _, files in os.walk(working_dir):
        for name in files:
            if name.endswith(".py") and not name.endswith(os.path.basename(__file__)):
                py_files_list.append(os.path.join(path, name))
    return py_files_list


def read_content_from_file(file_path):
    content = ""
    if os.path.exists(file_path.strip()):
        with open(file_path, 'r') as f:
            content = f.read()
            f.close()
    return content


def parse_file_content_as_entity(file_path, content):
    lines = content.split("\n")
    problem_entity = CodingProblemEntity(file_path)
    for line in lines:
        problem_leetcode_source = line.strip()
        if len(problem_leetcode_source) > len(leet_code_url) and problem_leetcode_source.find(leet_code_url) >= 0:
            # 找到一个新的leet code proble source
            problem_name = problem_leetcode_source[len(leet_code_url):]
            problem_name = problem_name.split("/")[1]
            problem_name_list = problem_name.split("-")
            if problem_name_list[-1] in same_problem_series:
                # 如果是变体题目，理论上应该都在一个文件夹内，此时problem_full_name需要删掉最后的题号
                problem_name_list.pop()
            for i, word in enumerate(problem_name_list):
                problem_name_list[i] = "%s%s" % (word[0].upper(), word[1:])
                if word[0] in '0123456789' and len(word) >= 2:
                    problem_name_list[i] = "%s%s%s" % (word[0], word[1].upper(), word[2:])
            problem_full_name = " ".join(problem_name_list)
            problem_entity.add_new_problem(problem_full_name)
    return problem_entity


def write_to_readme(readme_file_path, problem_entity_list):
    with open(readme_file_path, 'r') as readme_file:
        old_content = readme_file.read()
        readme_file.close()
    new_content_list = list([])
    for line in old_content.split("\n"):
        if len(line) > 6 and line[0:6] == "######":
            break
        new_content_list.append(line)
    new_content_list += problem_entity_list
    new_content = "\n".join(new_content_list)
    with open(readme_file_path, 'w') as readme_file:
        readme_file.write(new_content)
        readme_file.close()
    return len(new_content_list)


def batch(working_dir):
    all_file_paths = sorted(list_all_files(working_dir))
    problem_entity_list = list([])
    for file_path in all_file_paths:
        content = str(read_content_from_file(file_path))
        problem_entity = parse_file_content_as_entity(file_path[len(working_dir):], content)
        if len(problem_entity.problem_name_set):
            problem_entity_list.append(str(problem_entity))
    readme_file_path = os.path.join(working_dir, "README.md")
    total = write_to_readme(readme_file_path, problem_entity_list)
    print "%s lines in total in the new README.md" % total

if __name__ == '__main__':
    batch("../")
