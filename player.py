# -*- coding: utf-8 -*-
# File name: player.py
# Author: Changchang Ding
# Email: dingchan@indiana.edu
# Python Version: 3.5.2

import time
from multiprocessing import Process, Value

from board import Board


class InnerBoard(Board):
    def __init__(self, magic=None):
        super().__init__()
        self.value = 0

        self.magic = magic if magic is not None else [0, 1, 4, 9, 1000000]

    def generate_moves(self):
        # a simple re-order of moves, from center to border
        return [i for i in [3, 2, 4, 1, 5, 0, 6]
                if len(self.table[i]) < 6]

    def make_move(self, move):
        # rewrite this function, add evaluation of state
        self.history.append(move)
        column = self.table[move]

        delta_value = 0

        for c4 in self.ref_table[move][len(column)]:
            c4['value'][self.next_player] += 1

            # begin
            my_v = c4['value'][self.next_player]
            op_v = c4['value'][self.next_player ^ 1]
            if op_v != 0 and my_v == 1:
                delta_value += self.magic[op_v]
            elif op_v == 0:
                delta_value += self.magic[my_v] - self.magic[my_v - 1]
            # end

            if c4['value'][self.next_player] == 4:
                self.win = c4

        # begin
        self.value = delta_value - self.value
        # end

        column.append(self.next_player)
        self.next_player ^= 1

    def unmake_last_move(self):
        # rewrite this function, add evaluation of state
        last_move = self.history.pop()
        last_column = self.table[last_move]
        last_column.pop()
        self.next_player ^= 1

        delta_value = 0
        for c4 in self.ref_table[last_move][len(last_column)]:
            c4['value'][self.next_player] -= 1

            # begin
            my_v = c4['value'][self.next_player]
            op_v = c4['value'][self.next_player ^ 1]
            if op_v != 0 and my_v == 0:
                delta_value += self.magic[op_v]
            elif op_v == 0:
                delta_value += self.magic[my_v + 1] - self.magic[my_v]
            # end

        self.win = None

        # begin
        self.value = delta_value - self.value
        # end

    def make_permanent_move(self, move):
        # another variety of make_move, delete impossible c4's
        self.history.append(move)
        column = self.table[move]

        delta_value = 0
        impossible = []

        for c4 in self.ref_table[move][len(column)]:
            c4['value'][self.next_player] += 1
            my_v = c4['value'][self.next_player]
            op_v = c4['value'][self.next_player ^ 1]
            if op_v != 0 and my_v == 1:
                delta_value += self.magic[op_v - 1]
                impossible.append(c4)
            else:
                delta_value += self.magic[my_v] - self.magic[my_v - 1]
            if c4['value'][self.next_player] == 4:
                self.win = c4

        # remove impossible c4's
        # begin
        for stale_c4 in impossible:
            for c, r in stale_c4['positions']:
                for i, c4 in enumerate(self.ref_table[c][r]):
                    if c4['cid'] == stale_c4['cid']:
                        del self.ref_table[c][r][i]
                        break
        # end

        self.value = delta_value - self.value
        column.append(self.next_player)
        self.next_player ^= 1


class Player:
    def __init__(self, magic=None):
        self.magic = magic if magic is not None else [0, 1, 4, 9, 1000000]
        self.board = InnerBoard(self.magic)
        self.time = None

    def name(self):
        return 'Ursa Major'

    def make_move(self, move):
        self.time = time.time()
        self.board.make_permanent_move(move)

    def get_move(self):
        if self.time is None:
            self.time = time.time()
            make_move_time = 0.005
        else:
            make_move_time = time.time() - self.time

        best_move = Value('i', -1)
        p = Process(target=self.find_win_rec, args=(best_move,))
        p.start()
        p.join(2.99 - make_move_time - (time.time() - self.time))

        # The Player object will first be deep-copied in the child,
        # so terminate it won't break anything. No need to unmake all the moves.
        p.terminate()
        return best_move.value

    def find_win_rec(self, best_move):
        depth = 2
        while True:
            v, path = self.find_win(
                - self.magic[4] - 1, self.magic[4] + 1, depth)
            depth += 1
            best_move.value = path[-1]

    def find_win(self, a, b, depth):
        if self.board.last_move_won():
            return - self.magic[4], []
        if depth == 0:
            return - self.board.value, []
        moves = self.board.generate_moves()
        if len(moves) == 0:
            # Draw
            return 0, []

        best_path = []
        for move in moves:
            self.board.make_move(move)
            v, sub_path = self.find_win(- b, - a, depth - 1)
            v = - v
            self.board.unmake_last_move()
            if v >= b:
                return b, []
            if v > a:
                sub_path.append(move)
                best_path = sub_path
                a = v
        return a, best_path
