#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stockfish import Stockfish


fen_string = ""
with open('start.fen', 'r') as f:
    fen_string = f.readline()

print(fen_string)

pieces = {
    'K': "\u265A",
    'Q': "\u265B",
    'R': "\u265C",
    'B': "\u265D",
    'N': "\u265E",
    'P': "\u265F",

    'k': "\u2654",
    'q': "\u2655",
    'r': "\u2656",
    'b': "\u2657",
    'n': "\u2658",
    'p': "\u2659"
}

def print_board(fen_string):
    positions, _, _, _, _, _ = fen_string.split(' ')
    ranks = positions.split('/')

    global pieces

    for rank in ranks:
        for piece in rank:
            if piece in pieces:
                print(pieces[piece], end=' ')
            else:
                print('. ' * int(piece), end=' ')
        print()

print_board(fen_string)

stockfish = Stockfish()
current_position = []
while True:

    while not stockfish.is_move_correct(white_next_move := input("Whites next move: ")):
        pass

    current_position.append(white_next_move)
    stockfish.set_position(current_position)
    
    black_next_move = stockfish.get_best_move()
    current_position.append(black_next_move)
    stockfish.set_position(current_position)

    print("Black plays: " + black_next_move)
    print("Current position is: " + str(current_position))
