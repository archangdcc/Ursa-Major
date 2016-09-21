def perft(board, depth):
    if (board.last_move_won()):
        return 1

    moves = board.generate_moves()

    if len(moves) == 0:
        return 1

    if (depth == 1):
        return len(moves)

    n = 0
    for move in moves:
        board.make_move(move)
        n += perft(board, depth - 1)
        board.unmake_last_move()

    return n


def find_win_ab(board, a, b, depth):
    if board.last_move_won():
        return -1, []
    if depth == 0:
        return 0, []
    moves = board.generate_moves()
    if len(moves) == 0:
        return 0, []

    best_path = []
    for move in moves:
        board.make_move(move)
        v, sub_path = find_win_ab(board, - b, - a, depth - 1)
        v = - v
        board.unmake_last_move()
        if v >= b:
            return b, []
        if v > a:
            sub_path.append(move)
            best_path = sub_path
            a = v
    return a, best_path


def find_win(board, depth):
    v, path = find_win_ab(board, -2, 2, depth)
    print(path)
    if v == 1:
        return "WIN BY PLAYING {}".format(path[-1])
    elif v == -1:
        return "ALL MOVES LOSE"
    else:
        return "NO FORCED WIN IN {} MOVES".format(depth)
