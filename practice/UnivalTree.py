class TreeNode(object):
    def __init__(self, label, val, left=None, right=None):
        self.val = val
        self.label = label
        self.left = left
        self.right = right

    def __str__(self):
        return "{}=({})".format(self.label, self.val)


def recur(node, results):
    if node.left is None and node.right is None:
        return True
    leftSubtree = node.left is not None and recur(node.left, results)
    rightSubtree = node.right is not None and recur(node.right, results)
    if leftSubtree and rightSubtree:
        if node.val == node.left.val and node.val == node.right.val:
            return True
        results.append(node.left)
        results.append(node.right)
        return False
    if node.left and leftSubtree:
        results.append(node.left)
    if node.right and rightSubtree:
        results.append(node.right)

    return False


def findUnivalSubtree(root):
    results = list([])
    if recur(root, results):
        results.append(root)
    for res in results:
        print res
    print len(results)


def test1():
    root = TreeNode("root", 2)
    n1 = TreeNode("n1", 3)
    n2 = TreeNode("n2", 4)
    n3 = TreeNode("n3", 3)
    n4 = TreeNode("n4", 3)
    root.left = n1
    root.right = n2
    n1.left = n3
    n1.right = n4

    findUnivalSubtree(root)

test1()
