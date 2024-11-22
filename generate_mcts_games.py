import argparse
import numpy as np

from dljungle.encoders.base import get_encoder_by_name
from dljungle.jungleBoard import GameState, Board
from dljungle.mtcs import mcts
from dljungle.utils import print_board, print_move, custom_board

def generate_game(rounds, max_moves, temperature):
  boards, moves = [], []

  encoder = get_encoder_by_name('oneplane')

  board = Board()
  custom_board(board)
  game = GameState.new_game(board)

  bot = mcts.MCTSAgent(rounds, temperature)

  num_moves = 0
  while not game.is_over():
    print_board(game.board)
    move = bot.select_move(game)
    if move.is_play:
      boards.append(encoder.encode(game))

      # move_one_hot = np.zeros((2, encoder.num_points()))
      # move_one_hot[0, encoder.encode_point(move.prev_square.point)] = 1
      # dest_square = game.board.get_dest_square(move.prev_square, move.direction)
      # move_one_hot[1, encoder.encode_point(dest_square.point)] = 1
      # moves.append(move_one_hot)

      move_labels = np.zeros((encoder.num_points(), 4))
      label_x = encoder.encode_point(move.prev_square.point)
      label_y = 0
      if move.direction == "top":
        label_y = 0
      elif move.direction == "right":
        label_y = 1
      elif move.direction == "bot":
        label_y = 2
      else:
        label_y = 3
      move_labels[label_x, label_y] = 1
      moves.append(move_labels)

    print_move(game.next_player, move)
    game = game.apply_move(move)
    num_moves += 1
    if num_moves > max_moves:
      break
    print(f'Num Moves: {num_moves}')

  return np.array(boards), np.array(moves)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--rounds', '-r', type=int, default=1000)
  parser.add_argument('--temperature', '-t', type=float, default=0.8)
  parser.add_argument('--max-moves', '-m', type=int, default=100, help='Max moves per game')
  parser.add_argument('--num-games', '-n', type=int, default=100)
  parser.add_argument('--board-out')
  parser.add_argument('--move-out')

  args = parser.parse_args()

  for i in range(args.num_games):
      print('Generating game %d/%d...' % (i + 1, args.num_games))
      x, y = generate_game(args.rounds, args.max_moves, args.temperature)

      
      try:
        xs = np.load(args.board_out).tolist()
      except FileNotFoundError:
        xs = []

      try:
        ys = np.load(args.move_out).tolist()
      except FileNotFoundError:
        ys = []
        
      

      if len(xs) == 0:
        xs = x
        ys = y
      else:
        xs = np.concatenate((xs, x))
        ys = np.concatenate((ys, y))

      np.save(args.board_out, xs)
      np.save(args.move_out, ys)

      print("Save game Successful!")

    # except Exception as e:
    #   print(f"Some error when saving: {e}")

if __name__ == '__main__':
  main()