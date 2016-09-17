def _generate_win_positions():
    # All the possible connect-four's on the board
    col_positions = [[{'start': (c, r), 'direction': (0, 1), 'value': [0, 0]}
                      for r in range(3)] for c in range(7)]
    row_positions = [[{'start': (c, r), 'direction': (1, 0), 'value': [0, 0]}
                      for c in range(4)] for r in range(6)]
    cmr_positions = [
        [{'start': (0, 2), 'direction': (1, 1), 'value': [0, 0]}],
        [{'start': (0 + i, 1 + i), 'direction': (1, 1), 'value': [0, 0]}
         for i in range(2)],
        [{'start': (0 + i, 0 + i), 'direction': (1, 1), 'value': [0, 0]}
         for i in range(3)],
        [{'start': (1 + i, 0 + i), 'direction': (1, 1), 'value': [0, 0]}
         for i in range(3)],
        [{'start': (2 + i, 0 + i), 'direction': (1, 1), 'value': [0, 0]}
         for i in range(2)],
        [{'start': (3, 0), 'direction': (1, 1), 'value': [0, 0]}],
    ]
    cpr_positions = [
        [{'start': (3, 0), 'direction': (-1, 1), 'value': [0, 0]}],
        [{'start': (4 - i, 0 + i), 'direction': (-1, 1), 'value': [0, 0]}
         for i in range(2)],
        [{'start': (5 - i, 0 + i), 'direction': (-1, 1), 'value': [0, 0]}
         for i in range(3)],
        [{'start': (6 - i, 0 + i), 'direction': (-1, 1), 'value': [0, 0]}
         for i in range(3)],
        [{'start': (6 - i, 1 + i), 'direction': (-1, 1), 'value': [0, 0]}
         for i in range(2)],
        [{'start': (6, 2), 'direction': (-1, 1), 'value': [0, 0]}],
    ]
    return [
        col_positions,
        row_positions,
        cmr_positions,
        cpr_positions,
    ]


def _pick(m, n, k=4):
    return range(max(m - k + 1, 0), min(m + 1, n - k + 1))


class Board:
    def __init__(self):
        self.next_player = 0
        self.history = []
        self.columns = [[] for i in range(7)]
        self.win = None

        self.win_positions = _generate_win_positions()

        # Use pre-build reference table to reduce calculation
        self.ref_table = [[self._build_ref_table(c, r)
                           for r in range(6)] for c in range(7)]

    def _build_ref_table(self, col, row):
        # Return all the possible connect-four's that contain (col, row).
        retvar = []
        cpr = col - row
        cmr = col + row

        for i in _pick(row, 6):
            retvar.append(self.win_positions[0][col][i])

        for i in _pick(col, 7):
            retvar.append(self.win_positions[1][row][i])

        if cpr >= -2 and cpr <= 0:
            for i in _pick(col, 6 + cpr):
                retvar.append(self.win_positions[2][cpr + 2][i])
        elif cpr >= 1 and cpr <= 3:
            for i in _pick(row, 7 - cpr):
                retvar.append(self.win_positions[2][cpr + 2][i])

        if cmr >= 3 and cmr <= 5:
            for i in _pick(row, 1 + cmr):
                retvar.append(self.win_positions[3][cmr - 3][i])
        elif cmr >= 6 and cmr <= 8:
            for i in _pick(6 - col, 12 - cmr):
                retvar.append(self.win_positions[3][cmr - 3][i])
        return retvar

    def generate_moves(self):
        return [i for i in [3, 2, 4, 1, 5, 0, 6]
                if len(self.columns[i]) < 6]

    def make_move(self, move):
        self.history.append(move)
        column = self.columns[move]

        for pos in self.ref_table[move][len(column)]:
            pos['value'][self.next_player] += 1
            if pos['value'][self.next_player] == 4:
                self.win = pos
        column.append(self.next_player)
        self.next_player ^= 1

    def unmake_last_move(self):
        # assert(len(self.history) > 0)
        last_move = self.history.pop()
        last_column = self.columns[last_move]
        last_column.pop()
        self.next_player ^= 1

        for pos in self.ref_table[last_move][len(last_column)]:
            pos['value'][self.next_player] -= 1

        # Win will stop the game, so the previous move
        # of a win is always non-win.
        self.win = None

    def last_move_won(self):
        return self.win is not None

    def __str__(self):
        # An illustration:
        # 0/1 for the first/second play's move.
        # 'x' for empty tilde.

        state = [['' for j in range(7)] for i in range(6)]
        for i, column in enumerate(self.columns):
            j = 0
            while j < len(column):
                state[5 - j][i] = str(column[j])
                j += 1
            while j <= 5:
                state[5 - j][i] = 'x'
                j += 1

        if self.last_move_won():
            for c, r in self.win.positions:
                # Highlight the win position using ANSI code.
                state[5 - r][c] = '\x1b[1;31m{}\x1b[0m'.format(state[5 - r][c])

        return '\n'.join(
            [('|' + ' '.join(s) + '|') for s in state]
        ) + '\n---------------'
