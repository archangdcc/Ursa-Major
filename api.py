#!/usr/bin/env python3
# -*- coding: utf-8; -*-

import json

from flask import Flask, request

from player import Player


app = Flask(__name__)


@app.route('/um-api', methods=['POST'])
def get_move():
    moves = request.json.get('moves')
    player = Player()

    for move in moves:
        player.make_move(move)

    if player.board.last_move_won():
        return json.dumps(
            {'result': 0,
             'positions': player.board.win['positions']}
        )

    if len(player.board.generate_moves()) == 0:
        return json.dumps({'result': 1})

    move = player.get_move()
    player.make_move(move)

    if player.board.last_move_won():
        return json.dumps(
            {'result': 2,
             'move': move,
             'positions': player.board.win['positions']}
        )

    if len(player.board.generate_moves()) == 0:
        return json.dumps({'result': 1})

    return json.dumps({'move': move, 'result': -1})


if __name__ == '__main__':
    app.run()
