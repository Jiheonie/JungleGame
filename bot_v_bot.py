from dljungle import agent, jungleBoard
from dljungle.agent import mcts
from dljungle.jungleTypes import Square, Point, Player, Area, ChessMan, ChessType
from dljungle.utils import print_board, print_move
import time

SPECIAL_AREA = {
  (9, 4): [Player.RED, Area.CAVE],
  (9, 3): [Player.RED, Area.TRAP],
  (9, 5): [Player.RED, Area.TRAP],
  (8, 4): [Player.RED, Area.TRAP],
  (1, 4): [Player.GREEN, Area.CAVE],
  (1, 3): [Player.GREEN, Area.TRAP],
  (1, 5): [Player.GREEN, Area.TRAP],
  (2, 4): [Player.GREEN, Area.TRAP],
  (4, 2): [0, Area.RIVER],
  (4, 3): [0, Area.RIVER],
  (4, 5): [0, Area.RIVER],
  (4, 6): [0, Area.RIVER],
  (5, 2): [0, Area.RIVER],
  (5, 3): [0, Area.RIVER],
  (5, 5): [0, Area.RIVER],
  (5, 6): [0, Area.RIVER],
  (6, 2): [0, Area.RIVER],
  (6, 3): [0, Area.RIVER],
  (6, 5): [0, Area.RIVER],
  (6, 6): [0, Area.RIVER],
}

START_CHESS = {
  (1, 1): [Player.GREEN, ChessType.TIGER],
  (1, 7): [Player.GREEN, ChessType.LION],
  (2, 2): [Player.GREEN, ChessType.CAT],
  (2, 6): [Player.GREEN, ChessType.DOG],
  (3, 1): [Player.GREEN, ChessType.ELEPHANT],
  (3, 3): [Player.GREEN, ChessType.WOLF],
  (3, 5): [Player.GREEN, ChessType.LEOPARD],
  (3, 7): [Player.GREEN, ChessType.RAT],
  (9, 1): [Player.RED, ChessType.LION],
  (9, 7): [Player.RED, ChessType.TIGER],
  (8, 2): [Player.RED, ChessType.DOG],
  (8, 6): [Player.RED, ChessType.CAT],
  (7, 1): [Player.RED, ChessType.RAT],
  (7, 3): [Player.RED, ChessType.LEOPARD],
  (7, 5): [Player.RED, ChessType.WOLF],
  (7, 7): [Player.RED, ChessType.ELEPHANT],
}

def main():
  game = jungleBoard.GameState.new_game()

  # hard code place caves, traps, rivers
  for r in range(1, game.board.num_rows + 1):
    for c in range(1, game.board.num_cols + 1):
      square = Square(Point(r, c))
      if (r, c) in SPECIAL_AREA:
        player = SPECIAL_AREA.get((r, c))[0]
        area = SPECIAL_AREA.get((r, c))[1]
        square.set_area(player, area)
      if (r, c) in START_CHESS:
        chess = START_CHESS.get((r, c))
        chessman = ChessMan(chess[0], chess[1])
        game.board.add_square(square, chessman)
      else:
        game.board.add_square(square)
        
  bots = {
    Player.GREEN: mcts.RandomBot(),
    Player.RED: mcts.RandomBot(),
  }

  while not game.is_over():
    time.sleep(0.3)

    print(chr(27) + "[2J")
    bot_move = bots[game.next_player].select_move(game)
    if bot_move:
      print_board(game.board)
      print_move(game.next_player, bot_move)
      game = game.apply_move(bot_move)
      
  print(("green" if game.next_player == Player.RED else "red") + " win")

if __name__ == '__main__':
  main()