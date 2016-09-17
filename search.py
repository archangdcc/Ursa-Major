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


def find_win(board, depth):
    pass
