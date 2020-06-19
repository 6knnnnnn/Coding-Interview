from collections import deque


def bfs_zombies(matrix):
    queue = deque([])
    # create the starting point
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[i])):
            if matrix[i][j] == 1:
                queue.append([i, j])
    time = 0
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    while queue:
        size = len(queue)
        while size:
            size -= 1
            zombie = queue.popleft()
            for d in directions:
                row, col = zombie[0] + d[0], zombie[1] + d[1]
                if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]) and matrix[row][col] == 0:
                    # since it is next to a zombie, it will turn this round
                    matrix[row][col] = 1
                    queue.append([row, col])
        time += 1
    return time - 1


data = [
    [0, 1, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0]
]

print bfs_zombies(data)


