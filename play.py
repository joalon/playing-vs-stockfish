#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stockfish import Stockfish

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
  'p': "\u2659",
}

def fen_to_matrix(fen_string: str, pieces: dict, verbose:bool=False):
  positions, _, _, _, _, _ = fen_string.split(' ')
  ranks = positions.split('/')

  board = []

  for i, rank in enumerate(ranks):
    board.append([])
    for piece in rank:
      if piece in pieces:
        board[i].append(piece)
      else:
        for x in range(int(piece)):
          board[i].append('.')

  return list(reversed(board))

def rank_to_fen(rank):
  fen = ''
  count = 0
  for i in range(0, len(rank)):
    if rank[i] != '.':
      if count != 0:
        fen += str(count)
        count = 0
      fen += rank[i]
    else:
      count += 1

  if count != 0:
    fen += str(count)
  return fen

def matrix_to_fen(board: list) -> str:
  new_fen = ''

  for i in range(7, -1, -1):
    new_fen += rank_to_fen(board[i]) + '/'

  # Remove trailing slash in positions
  new_fen = new_fen[0:len(new_fen)-1]
  return new_fen
    
def move(fen_string: str, move: str) -> str:
  '''
  Takes a fen string and a move in algebraic notation and returns the resulting fen string.

  A move in algebraic chess notation might look like:
  e2e4  - Moves the piece at e2 to e4
  O-O   - Castles kingside
  d8Q   - Promote a pawn to a queen
  a1a8+ - Moves the piece at a1 to a8 and puts the other players king in check
  '''
  positions, current_player, current_castling_options, en_passant_target_square, current_half_move_count, current_full_moves = fen_string.split(' ')

  board = fen_to_matrix(fen_string, pieces, verbose=True)

  # Reset en passant square
  en_passant_target_square = '-'

  # Check if the move is castling
  if move == 'O-O':
    pass

  elif move == 'O-O-O':
    pass

  # Or if it's a pawn promotion
  elif len(move) == 3:
    pass

  # Otherwise move as usual
  else:
    # Algebraic movement string into matrix coordinates
    start_x = ord(move[0:1])-96-1
    start_y = int(move[1:2])-1
    end_x = ord(move[2:3])-96-1
    end_y = int(move[3:4])-1

    # Calculate en passant square
    if board[start_y][start_x] == 'p' or board[start_y][start_x] == 'P':
      if abs(end_y - start_y) == 2:
        if current_player == 'w':
          en_passant_target_square = chr(end_x + 97) + str(end_y)
        else:
          en_passant_target_square = chr(end_x + 97) + str(end_y+2)

    # Execute movement
    board[end_y][end_x] = board[start_y][start_x]
    board[start_y][start_x] = '.'

  # Calculate half moves since last capture
  if board[end_y][end_x] == '.':
    current_half_move_count = int(current_half_move_count) + 1
  else:
    current_half_move_count = 0

  # Construct next FEN string
  new_fen_positions = matrix_to_fen(board)
  next_player = 'w' if current_player == 'b' else 'b'
  next_move = int(current_full_moves)+1 if current_player == 'b' else int(current_full_moves)

  new_fen = f"{new_fen_positions} {next_player} {current_castling_options} {en_passant_target_square} {current_half_move_count} {next_move}"
  return new_fen

def print_board(fen_string: str) -> None:
    positions = fen_string.split(' ')[0]
    ranks = positions.split('/')

    global pieces

    for rank in ranks:
        for piece in rank:
            if piece in pieces:
                print(pieces[piece], end=' ')
            else:
                print('. ' * int(piece), end='')
        print()

fen_string = ""
with open('start.fen', 'r') as f:
    fen_string = f.readline()

print(fen_string)

# Tests
step1 = move(fen_string, "e2e4")
step2 = move(step1, "e7e5")
step3 = move(step2, "f2f4")
print(step3)


stockfish = Stockfish()
stockfish.set_fen_position(fen_string)
while True:

    print(fen_string)
    print_board(fen_string)

    print(f"Stockfish recommends {stockfish.get_best_move()}")

    while not stockfish.is_move_correct(white_next_move := input(f"Whites next move: ")):
        pass

    fen_string = move(fen_string, white_next_move)
    stockfish.set_fen_position(fen_string)

    black_next_move = stockfish.get_best_move()
    fen_string = move(fen_string, black_next_move)
    stockfish.set_fen_position(fen_string)



