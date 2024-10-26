from dljungle.jungleBoard import Board, GameState
from dljungle.mtcs.mcts import MCTSAgent
from dljungle.jungleTypes import Player, Point
from dljungle.utils import print_board, print_move, custom_board
import json


def main():
  print(chr(27) + "[2J")

  board = Board()
  custom_board(board)
  game = GameState.new_game(board)

  print_board(board)

  num_rounds = 50
        
  bots = {
    Player.GREEN: MCTSAgent(num_rounds, temperature=1.4),
    Player.RED: MCTSAgent(num_rounds, temperature=1.4),
  }

  step = 0
  data = {
    "steps": {},
    "result": None
  }

  while not game.is_over():

    init = {
      'next-player': "red" if game.next_player == Player.RED else "green",
      'state': {},
      'next-move': {},
    }

    print("---------------------------------------")
    print("Step " + str(step))

    bot_move = bots[game.next_player].select_move(game)
    for r in range(1, game.board.num_rows + 1):
      for c in range(1, game.board.num_cols + 1):
        chessman = game.board.get_chess_by_point(Point(r, c))
        if chessman:
          init["state"][f"{r}-{c}"] = {
            "player": "red" if chessman.player == Player.RED else "green",
            "chesstype": chessman.lost_power.value,
          }
        else:
          init["state"][f"{r}-{c}"] = {}

    if bot_move.is_play:
      init["next-move"] = {
        "row": bot_move.prev_square.point.row,
        "col": bot_move.prev_square.point.col,
        "direction": bot_move.direction,
      }
    else:
      init["next-move"] = {}

    data["steps"][str(step)] = init

    print_board(game.board)
    print_move(game.next_player, bot_move)
    game = game.apply_move(bot_move)

    step += 1

      
  print(game.winner)
  data["result"] = "red" if game.winner == Player.RED else "green"

  json_object = json.dumps(data, indent=4)

  with open("data_107.json", "w") as outfile:
    outfile.write(json_object)

if __name__ == '__main__':
  main()