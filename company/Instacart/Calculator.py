# Enter your code here. Read input from STDIN. Print output to STDOUT

"""
using a dict, key = var name, value: a var name, actual value

parse the input, the 1st line the target var, llines after that, process those lines -> dict
"""
import sys


def processVariables(line, cache):
    # valid input all the time
    line = line.split("=")
    if len(line) == 1:
        # first line
        s = line[0]
        if s[-1] == '\n':
            s = s[:len(s)]
        cache[s] = ""
    else:
        varName, varValue = line[0], line[1]
        varName = varName.strip()  # clean the trailing spaces
        varValue = varValue.strip()
        if varValue[-1] == '\n':
            varValue = varValue[:len(varValue)]
        cache[varName] = varValue


def evaluateVar(cache, target):
    while True:
        if target not in cache:
            return None
        value = cache[target]
        if value.isdigit():
            return value
        # the value is another variable, update the target
        target = value


def main():
    target = None
    firstLine = True
    lastLine = False
    cache = {}
    while True:
        line = sys.stdin.readline()
        if line[-1] != '\n':
            lastLine = True
        else:
            line = line.strip()
            # remove the last \n in the line
            line = line[:len(line)]
        # process this line into -> dict
        processVariables(line, cache)
        if firstLine:
            # if first line -> parse the target
            firstLine = False
            target = line
        if lastLine:
            break
    print cache
    print target
    res = evaluateVar(cache, target)
    print res


inputs = """T5
T1 = 1
T2 = 2
T3 = T5
T4 = T2
T5 = T1""".split("\n")

a = " 0 123\n"
a = a.strip()
print a, len(a)
