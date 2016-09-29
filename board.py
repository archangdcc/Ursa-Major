# -*- coding: utf-8 -*-
# File name: board.py
# Author: Changchang Ding
# Email: dingchan@indiana.edu
# Python Version: 3.5.2


def _get_c4(name, start, direction, cid):
    # return a dictionary contains info about this particular connect-four.
    positions = [
        (start[0] + i * direction[0], start[1] + i * direction[1])
        for i in range(4)
    ]

    return {
        'name': name,
        'start': start,
        'direction': direction,
        'value': [0, 0],  # positions occupied by each player
        'positions': positions,  # the four positions in a list
        'cid': cid
    }


def _generate_c4s():
    # All the possible connect-four's on the board
    c4 = []

    # Vertical
    direction = (0, 1)
    for c in range(7):
        for r in range(3):
            start = (c, r)
            name = 'V{}{}'.format(c, r)
            c4.append(_get_c4(name, start, direction, len(c4)))

    # Horizontal
    direction = (1, 0)
    for r in range(6):
        for c in range(4):
            start = (c, r)
            name = 'H{}{}'.format(r, c)
            c4.append(_get_c4(name, start, direction, len(c4)))

    # Diagonal
    direction = (1, 1)
    for j in range(3):
        for i in range(j + 1):
            name = 'D{}{}'.format(j, i)
            c4.append(_get_c4(name, (i, 2 - j + i), direction, len(c4)))
        for i in range(3 - j):
            name = 'D{}{}'.format(j + 3, i)
            c4.append(_get_c4(name, (j + i + 1, i), direction, len(c4)))

    # Back-Diagonal
    direction = (-1, 1)
    for j in range(3):
        for i in range(j + 1):
            name = 'B{}{}'.format(j, i)
            c4.append(_get_c4(name, (j - i + 3, i), direction, len(c4)))
        for i in range(3 - j):
            name = 'B{}{}'.format(j + 3, i)
            c4.append(_get_c4(name, (6 - i, i + j), direction, len(c4)))

    return c4


class Board:
    def __init__(self):
        self.next_player = 0
        self.history = []
        self.table = [[] for i in range(7)]
        self.win = None

        self.c4s = _generate_c4s()

        # Use pre-build reference table to reduce calculation
        self.ref_table = [[[] for r in range(6)] for c in range(7)]
        self._generate_ref_table()

    def _generate_ref_table(self):
        for c4 in self.c4s:
            for c, r in c4['positions']:
                self.ref_table[c][r].append(c4)

    def generate_moves(self):
        return [i for i in range(7)
                if len(self.table[i]) < 6]

    def make_move(self, move):
        self.history.append(move)
        column = self.table[move]

        for c4 in self.ref_table[move][len(column)]:
            c4['value'][self.next_player] += 1
            if c4['value'][self.next_player] == 4:
                self.win = c4
        column.append(self.next_player)
        self.next_player ^= 1

    def unmake_last_move(self):
        # assert(len(self.history) > 0)
        last_move = self.history.pop()
        last_column = self.table[last_move]
        last_column.pop()
        self.next_player ^= 1

        for c4 in self.ref_table[last_move][len(last_column)]:
            c4['value'][self.next_player] -= 1

        # Win will stop the game, so the previous move
        # of a win is always non-win.
        self.win = None

    def last_move_won(self):
        return self.win is not None

    def __str__(self):
        # An illustration:
        # 0/1 for the first/second play's move.
        # 'x' for empty position.

        state = [['' for j in range(7)] for i in range(6)]
        for c, column in enumerate(self.table):
            r = 0
            while r < len(column):
                state[5 - r][c] = str(column[r])
                r += 1
            while r <= 5:
                state[5 - r][c] = 'x'
                r += 1

        if self.win is not None:
            for c, r in self.win['positions']:
                # Highlight the win position using ANSI code.
                state[5 - r][c] = '\x1b[1;31m{}\x1b[0m'.format(state[5 - r][c])

        return '\n'.join(
            [('|' + ' '.join(s) + '|') for s in state]
        ) + '\n---------------'
