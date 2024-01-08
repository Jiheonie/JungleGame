from dljungle.jungleBoard import Board, GameState
from dljungle.mtcs.mcts import MCTSAgent
from dljungle.jungleTypes import Player
from dljungle.utils import print_board, print_move, custom_board


def main():
  print(chr(27) + "[2J")

  board = Board()
  custom_board(board)
  game = GameState.new_game(board)

  print_board(board)
        
  bots = {
    Player.GREEN: MCTSAgent(500, temperature=1.4),
    Player.RED: MCTSAgent(500, temperature=1.4),
  }

  while not game.is_over():

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