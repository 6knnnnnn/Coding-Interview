# Suppose we have a series of people relationships that looks something like this:
#        [    ['Bart',  'brother',   'Lisa'    ],
#            ['Bart',  'son',      'Homer'    ],
#            ['Marge', 'wife',     'Homer'    ],
#            ['Lisa',  'daughter', 'Homer'   ]    ]
#
#        i.e. inner lists have len == 3 and are in form name1, relationship, name2
#
# Given a series of relationships as a list of lists, and given two names, return
# all known "sequences" of relationships from name1 to name2
#
# e.g. with the lists above as input, with input names 'Bart' and 'Homer', you should return:
#    ['Bart son Homer', 'Bart brother Lisa daughter Homer']

from collections import defaultdict, deque


class FamilyGraph(object):
    def __init__(self, inputs):
        self.graph = defaultdict(dict)
        # pre process inputs to graph of members
        # use a 2 level nested map to represent the relations
        for input in inputs:
            name1, relation, name2 = input
            self.graph[name1][name2] = relation

    def findRelation(self, name1, name2):
        # return all possible relations between name1 and name2
        if name1 == name2:
            return []
        result = []
        # name + relation path so far
        queue = deque([(name1, [name1])])
        while queue:
            name, relation_path = queue.popleft()
            if name == name2:
                # find one relation path from name1 to name2
                result.append(" ".join(relation_path))
            else:
                relatives = self.graph[name]
                for rName, relation in relatives.items():
                    new_relation_path = list(relation_path)
                    new_relation_path.append(relation)
                    new_relation_path.append(rName)
                    queue.append((rName, new_relation_path))

        return result


def nocycle_test():
    inputs = [ ['Bart',  'brother',   'Lisa'    ],
               ['Bart',  'son',      'Homer'    ],
               ['Marge', 'wife',     'Homer'    ],
               ['Lisa',  'daughter', 'Homer'   ]]

    family = FamilyGraph(inputs)
    print family.findRelation("Bart", "Lisa")
    print family.findRelation("Bart", "Homer")


def cyclic_test():
    inputs = [
        ["A", "friend", "B"],
        ["B", "brother", "C"],
        ["C", "brother", "A"],
        ["A", "son", "D"],
        ["D", "father", "B"]
        # ["B", "brother", "A"],
    ]
    family = FamilyGraph(inputs)
    members = ["A", "B", "C", "D"]
    for i in members:
        for j in members:
            print i, j, ": ", family.findRelation(i, j)

cyclic_test()



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

    def findRelation(self, name1, name2):
        # return all possible relations between name1 and name2
        result = []
        # name + relation path so far
        queue = deque([(name1, [name1])])
        while queue:
            name, relation_path = queue.popleft()
            if name == name2:
                # find one relation path from name1 to name2
                result.append(" ".join(relation_path))
            else:
                relatives = self.graph[name]
                for rName, relations in relatives.items():
                    for relation in relations:
                        new_relation_path = list(relation_path)
                        new_relation_path.append(relation)
                        new_relation_path.append(rName)
                        queue.append((rName, new_relation_path))

        return result


def nocycle_dup_test():
    inputs = [ ['Bart',  'brother',   'Lisa'    ],
               ['Bart',  'son',      'Homer'    ],
               ['Marge', 'wife',     'Homer'    ],
               ['Lisa',  'daughter', 'Homer'   ],
               ['Bart', 'friend', 'Homer']
               ]

    family = FamilyGraphDuplicates(inputs)
    print family.findRelation("Bart", "Lisa")
    print family.findRelation("Bart", "Homer")


nocycle_dup_test()
