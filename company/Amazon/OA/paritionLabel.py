def partitionLabels(S):
    # https://leetcode.com/problems/partition-labels
    lastIndex = {c: i for i, c in enumerate(S)}
    # two pointers
    left = right = 0
    results = []
    for i, c in enumerate(S):
        right = max(right, lastIndex[c])
        if i == right:
            # find one partition
            partition = S[left: right+1]
            results.append(len(partition))
            left = i + 1

    print results


partitionLabels("ababcbacadefegdehijhklij")
partitionLabels("a")
a = range(10)
for i, c in enumerate(a):
    print i,c


def lengthEachScene(inputList):
    # first preprocess the input list
    # use a map to record the last index of a char in the input
    lastIndex = {}
    for i, c in enumerate(inputList):
        lastIndex[c] = i

    # now use two pointers to iterate the input list
    left = right = 0
    results = []
    for i, c in enumerate(inputList):
        # compare the right index of current char with its very last index
        right = max(right, lastIndex[c])
        if i == right:
            # if this right pointer is also the last one, we find one partition
            partition = inputList[left: right + 1]
            results.append(len(partition))
            # move to the next parition by moving the left pointer to i + 1
            left = i + 1
    return results