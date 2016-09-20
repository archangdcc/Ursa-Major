#!/usr/bin/env python3
import random
import sys
import time
import profile

import board
import player
import random_player
import search


b = board.Board()


def test_0(b=board.Board()):
    state = [['' for j in range(7)] for i in range(6)]
    for c, column in enumerate(b.ref_table):
        for r, row in enumerate(column):
            state[5 - r][c] = "{:2d}".format(len(row))
            temp = []
            for c4 in row:
                try:
                    assert((c, r) in c4['positions'])
                except:
                    print(c4['name'])
                    exit()
                temp.append(c4['name'])
            print('{}{}: {}'.format(c, r, '; '.join(temp)))

    print()
    print('\n'.join(
        [('|' + ' '.join(s) + '|') for s in state]
    ) + '\n----------------------')


def test_profile():
    # search.perft(b, 8)
    search.find_win(b, 8)


def test_5():
    for k in range(1000):
        i = 0
        b = board.Board()
        while not b.last_move_won() and len(b.generate_moves()) > 0:
            moves = b.generate_moves()
            move = random.choice(moves)
            b.make_permanent_move(move)
            i += 1

        state = [['' for j in range(7)] for i in range(6)]
        for c, column in enumerate(b.ref_table):
            for r, row in enumerate(column):
                state[5 - r][c] = "{:2d}".format(len(row))
                temp = []
                for c4 in row:
                    try:
                        assert((c, r) in c4['positions'])
                    except:
                        print(c4['name'])
                        exit()
                    temp.append(c4['name'])
                print('{}{}: {}'.format(c, r, '; '.join(temp)))

        print()
        print('\n'.join(
            [('|' + ' '.join(s) + '|') for s in state]
        ) + '\n----------------------')
        print(b)
        print("============================================")


def test_find_win():
    for depth in range(3, 9):
        b = board.Board()
        t0 = time.time()
        search.find_win(b, depth, "dfs")
        t1 = time.time()
        print("{} s".format(t1 - t0))


def test_Q1():
    print("TESTING FOR Q1")
    b = board.Board()
    init_str = str(b)

    # test move generator in initial position
    assert(b.generate_moves() == [0, 1, 2, 3, 4, 5, 6])

    # test last_move_won in initial position
    assert(b.last_move_won() == False)
    b.make_move(0)
    b.make_move(1)
    b.make_move(0)
    b.make_move(1)
    b.make_move(0)
    b.make_move(1)
    b.make_move(0)

    # test last_move_won in simple position
    assert(b.last_move_won() == True)
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()
    b.unmake_last_move()

    # test the unmake operates correctly (assuming __str__() is correct)
    assert(init_str == str(b))

    # play 1000 random games to test make/unmake return board to start state
    for k in range(1000):
        i = 0
        while not b.last_move_won() and len(b.generate_moves()) > 0:
            moves = b.generate_moves()
            move = random.choice(moves)
            b.make_move(move)
            i += 1

        print(b)
        print(b.last_move_won())
        print('================================')

        for j in range(i):
            b.unmake_last_move()
        assert(init_str == str(b))
    print("passed")


def test_Q2():
    print("TESTING FOR Q2")
    b = board.Board()
    assert(search.perft(b, 1) == 7)
    t0 = time.time()
    assert(search.perft(b, 7) == 823536)
    t1 = time.time()
    print("{} s".format(t1 - t0))
    assert(search.perft(b, 8) == 5686266)
    t2 = time.time()
    print("{} s".format(t2 - t1))
    b.make_move(0)
    b.make_move(2)
    b.make_move(0)
    assert(search.perft(b, 8) == 5245276)
    t3 = time.time()
    print("{} s".format(t3 - t2))
    print("passed")


def test_Q3():
    print("TESTING FOR Q3")
    b = board.Board()
    t0 = time.time()
    assert(search.find_win(b, 8) == "NO FORCED WIN IN 8 MOVES")
    t1 = time.time()
    print("{} s".format(t1 - t0))
    b.make_move(2)
    b.make_move(0)
    b.make_move(3)
    b.make_move(0)
    assert(search.find_win(b, 3) == "WIN BY PLAYING 4")
    b.make_move(4)
    assert(search.find_win(b, 3) == "ALL MOVES LOSE")
    print("passed")


def test_Q4():
    players = [player.Player(), random_player.Player()]
    random.shuffle(players)
    print(players[0].name() + " vs " + players[1].name())

    b = board.Board()
    i = 0
    legal_moves = b.generate_moves()
    while not b.last_move_won() and len(legal_moves) > 0:
        move = players[i].get_move()
        players[0].make_move(move)
        players[1].make_move(move)
        b.make_move(move)
        i ^= 1
        legal_moves = b.generate_moves()
    if b.last_move_won():
        print("VICTORY FOR PLAYER " + players[i ^ 1].name())
    else:
        print("DRAW")


if __name__ == '__main__':
    if sys.argv[1] == 'all':
        test_Q1()
        test_Q2()
        test_Q3()
        test_Q4()
    elif sys.argv[1] == '1':
        test_Q1()
    elif sys.argv[1] == '2':
        test_Q2()
    elif sys.argv[1] == '3':
        test_Q3()
    elif sys.argv[1] == '4':
        test_Q4()
    elif sys.argv[1] == '0':
        test_0()
    elif sys.argv[1] == '5':
        test_5()
    elif sys.argv[1] == 'p':
        profile.run("test_profile()")
    elif sys.argv[1] == 'w':
        test_find_win()
