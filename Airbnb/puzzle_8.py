import heapq


def dis(x, y):  # A* evaluation func
    return (x - 2) ** 2 + (y - 2) ** 2


def play(board):
    m, n = len(board), len(board[0])
    x, y = 0, 0
    for i in xrange(m):
        for j in xrange(n):
            if board[i][j] == ' ':
                x, y = i, j
    board_repr = ''.join(''.join(row) for row in board)
    heap = [(dis(x, y), x, y, board_repr)]
    visited = set()
    # use a heap, where key is the distance of this element to its right index

    while heap:
        _, x, y, cur_repr = heapq.heappop(heap)
        if cur_repr in visited:
            continue
        visited.add(cur_repr)
        if cur_repr == "12345678 ":
            return True
        for dx, dy in zip((1, -1, 0, 0), (0, 0, 1, -1)):
            # up, down, right, left
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < m and 0 <= new_y < n:
                pos1, pos2 = x * m + y, new_x * m + new_y
                new_board = list(cur_repr)
                # swap, pos1 and pos2 is the sequential index in list of board repr
                new_board[pos1], new_board[pos2] = new_board[pos2], new_board[pos1]
                heapq.heappush(heap, (dis(new_x, new_y), new_x, new_y, ''.join(new_board)))

    return False
