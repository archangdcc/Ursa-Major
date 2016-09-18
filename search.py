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
        return -1
    if depth == 0:
        return 0
    moves = board.generate_moves()
    if len(moves) == 0:
        return 0
    for move in moves:
        board.make_move(move)
        v = - find_win_ab(board, - b, - a, depth - 1)
        board.unmake_last_move()
        if v >= b:
            return b
        if v > a:
            a = v
    return a


def find_win(board, depth):
    no_result = False
    for move in board.generate_moves():
        board.make_move(move)
        lose = find_win_ab(board, -2, 2, depth - 1)
        board.unmake_last_move()
        if lose == -1:
            return "WIN BY PLAYING {}".format(move)
        elif lose == 0:
            no_result = True

    if no_result:
        return "NO FORCED WIN IN {} MOVES".format(depth)
    else:
        return "ALL MOVES LOSE"
