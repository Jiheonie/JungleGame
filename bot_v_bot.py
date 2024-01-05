from dljungle import jungleBoard
from dljungle.agent import naive
from dljungle.jungleTypes import Player
from dljungle.utils import print_board, print_move, custom_board
import time


def main():
  print(chr(27) + "[2J")

  game = jungleBoard.GameState.new_game()

  custom_board(game.board)
        
  bots = {
    Player.GREEN: naive.RandomBot(),
    Player.RED: naive.RandomBot(),
  }

  while not game.is_over():
    time.sleep(0.3)

    print(chr(27) + "[2J")
    bot_move = bots[game.next_player].select_move(game)
    if bot_move:
      print_board(game.board)
      print_move(game.next_player, bot_move)
      game = game.apply_move(bot_move)
      
  print(game.winner)

if __name__ == '__main__':
  main()