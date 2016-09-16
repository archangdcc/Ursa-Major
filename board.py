class WinPosition:
    # A possible connet-four on the board
    def __init__(self, name):
        self.player = None
        self.value = 0
        self.con_value = 0
        self.name = name

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
            self.player = None

    def win(self):
        return self.value == 4

    def impossible(self):
        return self.con_value != 0

    def __str__(self):
        return "{}:{}-{}/{}".format(
            self.name,
            self.player if self.player is not None else 'X',
            self.value,
            self.con_value
        )


def _generate_win_positions():
    # All the possible connect-four's on the board
    col_positions = [[WinPosition("C{}{}".format(i, j))
                      for j in range(3)] for i in range(7)]
    row_positions = [[WinPosition("R{}{}".format(i, j))
                      for j in range(4)] for i in range(6)]
    cmr_positions = [
        [WinPosition("M-2{}".format(i)) for i in range(1)],
        [WinPosition("M-1{}".format(i)) for i in range(2)],
        [WinPosition("M+0{}".format(i)) for i in range(3)],
        [WinPosition("M+1{}".format(i)) for i in range(3)],
        [WinPosition("M+2{}".format(i)) for i in range(2)],
        [WinPosition("M+3{}".format(i)) for i in range(1)],
    ]
    cpr_positions = [
        [WinPosition("P3{}".format(i)) for i in range(1)],
        [WinPosition("P4{}".format(i)) for i in range(2)],
        [WinPosition("P5{}".format(i)) for i in range(3)],
        [WinPosition("P6{}".format(i)) for i in range(3)],
        [WinPosition("P7{}".format(i)) for i in range(2)],
        [WinPosition("P8{}".format(i)) for i in range(1)],
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

    if cpr > -3 and cpr < 1:
        for i in _pick(row, 6 + cpr):
            retvar.append((2, cpr + 2, i))
    elif cpr > 0 and cpr < 4:
        for i in _pick(col, 7 - cpr):
            retvar.append((2, cpr + 2, i))

    if cmr > 2 and cmr < 6:
        for i in _pick(row, 1 + cmr):
            retvar.append((3, cmr - 3, i))
    elif cmr > 5 and cmr < 9:
        for i in _pick(col, 12 - cmr):
            retvar.append((3, cmr - 3, i))
    return retvar


class Board:
    def __init__(self):
        self.player = 1
        self.history = []
        self.columns = [[] for i in range(7)]
        self.win = None

        self.win_positions = _generate_win_positions()
        self.ref_table = [
            [_build_ref_table(c, r) for r in range(6)]
            for c in range(7)
        ]

    def get_win_positions(self, col, row):
        retvar = []
        indexes = self.ref_table[col][row]
        for i, j, k in indexes:
            retvar.append(self.win_positions[i][j][k])
        return retvar

    def generate_moves(self):
        moves = []
        for i, column in enumerate(self.columns):
            if (len(column) < 5):
                moves.append(i)
        return moves

    def make_move(self, move):
        # assert(!self.win())
        self.player ^= 1
        column = self.columns[move]
        # assert(len(column) < 5)
        column.append(self.player)
        for pos in self.get_win_positions(move, len(column)):
            pos.push(self.player)
        self.history.append(move)

        for p in self.get_win_positions(move, len(column)):
            if p.win():
                self.win = self.player
                break

    def unmake_last_move(self):
        # assert(len(self.history) > 0)
        last_move = self.history.pop()
        last_column = self.columns[last_move]
        self.player ^= 1
        for pos in self.get_win_positions(last_move, len(last_column)):
            pos.pop(self.player)
        last_column.pop()

        # Win will stop the game, so the last move of a win is always non-win.
        self.win = None

    def last_move_won(self):
        return self.win is not None

    def __str__(self):
        state = [['' for j in range(7)] for i in range(6)]
        for i, column in enumerate(self.columns):
            j = 0
            while j < len(column):
                state[5 - j][i] = str(column[j])
                j += 1
            while j <= 5:
                state[5 - j][i] = 'x'
                j += 1
        return '\n'.join(
            [('|' + ' '.join(s) + '|') for s in state]
        ) + '\n---------------'
