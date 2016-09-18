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


def find_win_ab(board, a, b, depth, path):
    if board.last_move_won():
        return -1, path
    if depth == 0:
        return 0, path
    moves = board.generate_moves()
    if len(moves) == 0:
        return 0, path

    best_path = []
    for move in moves:
        board.make_move(move)
        v, sub_path = find_win_ab(board, - b, - a, depth - 1, [move])
        v = - v
        board.unmake_last_move()
        if v >= b:
            return b, path
        if v > a:
            best_path = sub_path
            a = v
    path.extend(best_path)
    return a, path


def find_win(board, depth):
    v, path = find_win_ab(board, -2, 2, depth, [])
    if v == 1:
        return "WIN BY PLAYING {}".format(path[0])
    elif v == -1:
        return "ALL MOVES LOSE"
    else:
        return "NO FORCED WIN IN {} MOVES".format(depth)
