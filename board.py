class WinPosition:
    # A possible connect-four on the board
    def __init__(self, start, direction):
        self.player = None
        self.value = 0
        self.con_value = 0

        self.start = start
        self.direction = direction
        self.positions = [start]
        for i in range(1, 4):
            self.positions.append(
                (start[0] + i * direction[0],
                 start[1] + i * direction[1])
            )
        if direction == (0, 1):
            self.catelog = "C"
        elif direction == (1, 0):
            self.catelog = "R"
        elif direction == (1, 1):
            self.catelog = "M"
        elif direction == (-1, 1):
            self.catelog = "P"

    def push(self, player):
        if self.player is None:
            self.player = player
            self.value = 1
        elif self.player == player:
            self.value += 1
        else:
            self.con_value += 1

    def pop(self, player):
        if self.player == player:
            self.value -= 1
        else:
            self.con_value -= 1
        if self.value == 0:
            assert(self.con_value == 0)
            self.player = None

    def win(self):
        return self.value == 4

    def impossible(self):
        return self.con_value != 0

    def __str__(self):
        return "{}{}{}:{}-{}/{}".format(
            self.catelog,
            self.start[0],
            self.start[1],
            self.player if self.player is not None else 'X',
            self.value,
            self.con_value
        )


def _generate_win_positions():
    # All the possible connect-four's on the board
    col_positions = [[WinPosition((c, r), (0, 1))
                      for r in range(3)] for c in range(7)]
    row_positions = [[WinPosition((c, r), (1, 0))
                      for c in range(4)] for r in range(6)]
    cmr_positions = [
        [WinPosition((0, 2), (1, 1))],
        [WinPosition((0 + i, 1 + i), (1, 1)) for i in range(2)],
        [WinPosition((0 + i, 0 + i), (1, 1)) for i in range(3)],
        [WinPosition((1 + i, 0 + i), (1, 1)) for i in range(3)],
        [WinPosition((2 + i, 0 + i), (1, 1)) for i in range(2)],
        [WinPosition((3, 0), (1, 1))],
    ]
    cpr_positions = [
        [WinPosition((3, 0), (-1, 1))],
        [WinPosition((4 - i, 0 + i), (-1, 1)) for i in range(2)],
        [WinPosition((5 - i, 0 + i), (-1, 1)) for i in range(3)],
        [WinPosition((6 - i, 0 + i), (-1, 1)) for i in range(3)],
        [WinPosition((6 - i, 1 + i), (-1, 1)) for i in range(2)],
        [WinPosition((6, 2), (-1, 1))],
    ]
    return [
        col_positions,
        row_positions,
        cmr_positions,
        cpr_positions,
    ]


def _pick(m, n, k=4):
    return range(max(m - k + 1, 0), min(m + 1, n - k + 1))


def _build_ref_table(col, row):
    # Return all the possible connect-four's that contain (col, row).
    retvar = []
    cpr = col - row
    cmr = col + row

    for i in _pick(row, 6):
        retvar.append((0, col, i))

    for i in _pick(col, 7):
        retvar.append((1, row, i))

    if cpr >= -2 and cpr <= 0:
        for i in _pick(row, 6 + cpr):
            retvar.append((2, cpr + 2, i))
    elif cpr >= 1 and cpr <= 3:
        for i in _pick(col, 7 - cpr):
            retvar.append((2, cpr + 2, i))

    if cmr >= 3 and cmr <= 5:
        for i in _pick(row, 1 + cmr):
            retvar.append((3, cmr - 3, i))
    elif cmr >= 6 and cmr <= 8:
        for i in _pick(col, 12 - cmr):
            retvar.append((3, cmr - 3, i))
    return retvar


class Board:
    def __init__(self):
        self.player = 1  # this player, not the next player
        self.history = []
        self.columns = [[] for i in range(7)]
        self.win = None

        self.win_positions = _generate_win_positions()

        # Use lookup table to reduce calculation
        self.ref_table = [[_build_ref_table(c, r) for r in range(6)]
                          for c in range(7)]

    def get_win_positions(self, col, row):
        retvar = []
        indexes = self.ref_table[col][row]
        for i, j, k in indexes:
            retvar.append(self.win_positions[i][j][k])
        return retvar

    def generate_moves(self):
        moves = []
        for i, column in enumerate(self.columns):
            if (len(column) < 6):
                moves.append(i)
        return moves

    def make_move(self, move):
        # assert(!self.win())
        self.player ^= 1
        self.history.append(move)
        column = self.columns[move]
        # assert(len(column) < 6)

        for pos in self.get_win_positions(move, len(column)):
            pos.push(self.player)

        for p in self.get_win_positions(move, len(column)):
            if p.win():
                self.win = p
                break
        column.append(self.player)

    def unmake_last_move(self):
        # assert(len(self.history) > 0)
        last_move = self.history.pop()
        last_column = self.columns[last_move]
        last_column.pop()

        for pos in self.get_win_positions(last_move, len(last_column)):
            pos.pop(self.player)
        self.player ^= 1

        # Win will stop the game, so the previous move
        # of a win is always non-win.
        self.win = None

    def last_move_won(self):
        return self.win is not None

    def __str__(self):
        # An illustration:
        # 0/1 for the first/second play's move.
        # 'x' for empty tilde.
        # Highlight the win position using ANSI code.

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
                state[5 - r][c] = '\x1b[1;31m{}\x1b[0m'.format(state[5 - r][c])

        return '\n'.join(
            [('|' + ' '.join(s) + '|') for s in state]
        ) + '\n---------------'
