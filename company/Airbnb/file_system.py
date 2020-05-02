# -*- coding: utf-8 -*-


def hello_world():
    print "Yes hello world"


def hello_world_no():
    print "No hello world"


class TreeNode(object):
    def __init__(self, key):
        self.key = key
        self.value = None
        self.child_map = dict([])
        self.function = None

    def update_function(self, function):
        self.function = function

    def add_new_child(self, key):
        child = TreeNode(key)
        self.child_map[key] = child

    def has_key_child(self, key):
        return key in self.child_map

    def get_key_child(self, key):
        return self.child_map.get(key)

    def __repr__(self):
        return "%s: %s, %s of child-node" % (self.key, self.value, len(self.child_map))


class FileSystem(object):
    def __init__(self):
        self.root = TreeNode("root")

    def create(self, path, value):
        path_list = path.split("/")
        node = self.root
        for p in path_list:
            if not node.has_key_child(p):
                node.add_new_child(key=p)
            node = node.get_key_child(p)
            if node.function:
                node.function()
        node.value = value

    def set_value(self, path, value):
        path_list = path.split("/")
        node = self.root
        for p in path_list:
            if not node.has_key_child(p):
                return False
            node = node.get_key_child(p)
        node.value = value
        return True

    def get_value(self, path):
        path_list = path.split("/")
        node = self.root
        for p in path_list:
            if not node.has_key_child(p):
                return None
            node = node.get_key_child(p)
        return node.value

    def watch(self, path, function):
        path_list = path.split("/")
        node = self.root
        for p in path_list:
            if not node.has_key_child(p):
                return None
            node = node.get_key_child(p)
        node.update_function(function)

FS = FileSystem()
FS.create("NA/CA", 1)
FS.create("NA/MX", 3)
FS.create("NA/US", 2)

FS.watch("NA/US", hello_world)
FS.create("NA/US/NY", 0)
FS.create("NA/US/FL", 20)

print FS.set_value("NA/US/NY", 10)
print FS.set_value("NA/US/WA", 0)

print FS.get_value("NA/US/WA")
print FS.get_value("NA/US/NY")
print FS.get_value("NA/MX")

