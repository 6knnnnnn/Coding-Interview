# Suppose we have a series of people relationships that looks something like this:
#        [    ['Bart',  'brother',   'Lisa'    ],
#            ['Bart',  'son',      'Homer'    ],
#            ['Marge', 'wife',     'Homer'    ],
#            ['Lisa',  'daughter', 'Homer'   ]    ]
#
#        i.e. inner lists have len == 3 and are in form startName, relationship, endName
#
# Given a series of relationships as a list of lists, and given two inputs, return
# all known "sequences" of relationships from startName to endName
#
# e.g. with the lists above as input, with input inputs 'Bart' and 'Homer', you should return:
#    ['Bart son Homer', 'Bart brother Lisa daughter Homer']

from collections import defaultdict


class FamilyGraph(object):
    def __init__(self, inputs):
        self.graph = defaultdict(dict)
        # pre process inputs to graph of members
        # use a 2 level nested map to represent the relations
        for input in inputs:
            name1, relation, name2 = input
            self.graph[name1][name2] = relation

    def dfs(self, name, endName):
        if name == endName:
            self.result.append(' '.join(self.relation_path))
            return

        if name in self.graph:
            self.visited.add(name)
            for adjName, relation in self.graph[name].items():
                if adjName not in self.visited:
                    newRP = "{} {}".format(relation, adjName)
                    self.relation_path.append(newRP)
                    self.dfs(adjName, endName)
                    self.relation_path.pop()
            self.visited.remove(name)

    def dfsCache(self, name, endName, cache):
        if name == endName:
            self.result.append(' '.join(self.relation_path))
            return

        if name in self.graph:
            self.visited.add(name)
            for adjName, relation in self.graph[name].items():
                if adjName not in self.visited:
                    if adjName in cache and endName in cache[adjName]:
                    # cache stores all the paths from name to endName
                        cachedPaths = cache[adjName][endName]
                    else:
                        newRP = "{} {}".format(relation, adjName)
                        self.relation_path.append(newRP)
                        self.dfs(adjName, endName)
                        cachedPaths[adjName][endName] = []
                        self.relation_path.pop()
            self.visited.remove(name)


    def findRelation(self, startName, endName):
        if startName == endName or startName not in self.graph:
            return []
        self.visited = set([])
        self.relation_path = list([])
        self.result = []
        self.relation_path = []
        self.dfs(startName, endName)
        for i in xrange(len(self.result)):
            self.result[i] = "{} {}".format(startName, self.result[i])
        return self.result


def test1():
    inputs = [ ['Bart',  'brother',   'Lisa'    ],
               ['Bart',  'son',      'Homer'    ],
               ['Marge', 'wife',     'Homer'    ],
               ['Lisa',  'daughter', 'Homer'   ]]

    family = FamilyGraph(inputs)
    print family.findRelation("Bart", "Lisa")
    print family.findRelation("Bart", "Homer")
    inputs = [
        ["A", "ab", "B"],
        ["B", "bc", "C"],
        ["C", "ca", "A"],
        ["A", "ad", "D"],
        ["D", "db", "B"]
    ]
    family = FamilyGraph(inputs)
    members = ["A", "B", "C", "D"]
    for i in members:
        for j in members:
            print i, j, ": ", family.findRelation(i, j)


class FamilyGraphDuplicates(object):
    def __init__(self, inputs):
        self.graph = defaultdict(dict)
        # pre process inputs to graph of members
        # use a 2 level nested map to represent the relations
        for input in inputs:
            name1, relation, name2 = input
            if name2 not in self.graph[name1]:
                self.graph[name1][name2] = list([])
            self.graph[name1][name2].append(relation)

    def dfs(self, name, endName):
        if name == endName:
            self.result.append(' '.join(self.relation_path))
            return

        if name in self.graph:
            self.visited.add(name)
            for adjName, relation_list in self.graph[name].items():
                if adjName not in self.visited:
                    for relation in relation_list:
                        newRP = "{} {}".format(relation, adjName)
                        self.relation_path.append(newRP)
                        self.dfs(adjName, endName)
                        self.relation_path.pop()
            self.visited.remove(name)

    def findRelation(self, startName, endName):
        if startName == endName or startName not in self.graph:
            return []
        self.visited = set([])
        self.relation_path = list([])
        self.result = []
        self.relation_path = []
        self.dfs(startName, endName)
        for i in xrange(len(self.result)):
            self.result[i] = "{} {}".format(startName, self.result[i])
        return self.result


def test2():
    inputs = [
        ["A", "ab1", "B"],
        ["A", "ab2", "B"],
        ["A", "ab3", "B"],
        ["B", "bc", "C"],
        ["C", "ca", "A"],
        ["A", "ad1", "D"],
        ["A", "ad2", "D"],
        ["D", "db", "B"]
    ]
    family = FamilyGraphDuplicates(inputs)
    members = ["A", "B", "C", "D"]
    for i in members:
        for j in members:
            print i, j, ": ", family.findRelation(i, j)


test2()
