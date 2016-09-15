import random


class Player:
    def __init__(self):
        # counts stores how many tiles are in each column (initalised to 0)
        self.counts = [0] * 7

    def name(self):
        return 'RANDOM'

    def make_move(self, move):
        # every time a move is made the number of tiles
        # in that column increases by one
        self.counts[move] += 1

    def get_move(self):
        # first we generate the moves, which is any column
        # that isn't full (has less than 6 tiles)
        moves = []
        for i in range(0, 7):
            if self.counts[i] < 6:
                moves.append(i)
        # return a random legal move
        return random.choice(moves)
