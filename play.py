#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stockfish import Stockfish



pieces = {
    'White king': "\u265A",
    'Black king': "\u2654",
}



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
