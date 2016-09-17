# import random
#
# import board


def perft(board, depth):
    if (board.last_move_won() or depth == 0):
        return 1

    moves = board.generate_moves()
    if len(moves) == 0:
        return 1

    n = 0
    for move in moves:
        board.make_move(move)
        n += perft(board, depth - 1)
        board.unmake_last_move()

    return n


def find_win(board, depth):
    pass
