from dljungle.jungleBoard import Board, GameState
from dljungle.minimax import minimax
from dljungle.jungleTypes import Player
from dljungle.utils import print_board, print_move, custom_board
import time


def main():
  print(chr(27) + "[2J")

  board = Board()
  custom_board(board)
  game = GameState.new_game(board)

  print_board(board)
        
  bots = {
    Player.GREEN: minimax.MinimaxAgent(),
    Player.RED: minimax.MinimaxAgent(),
  }

  while not game.is_over():
    # time.sleep(0.3)

    # print(chr(27) + "[2J")
    print("---------------------------------------")
    bot_move = bots[game.next_player].select_move(game)
    if bot_move:
      print_board(game.board)
      print_move(game.next_player, bot_move)
      game = game.apply_move(bot_move)
      
  print(game.winner)

if __name__ == '__main__':
  main()