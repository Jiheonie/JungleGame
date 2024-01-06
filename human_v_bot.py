from dljungle import agent, jungleBoard
from dljungle.agent import naive
from dljungle.jungleTypes import Square, Point, Player, Area, ChessMan, ChessType
from dljungle.utils import print_board, print_move, point_from_coords, custom_board
from six.moves import input

def main():
  print(chr(27) + "[2J")

  game = jungleBoard.GameState.new_game()
  custom_board(game.board)
  game.set_legal_moves()
  bot = agent.naive.RandomBot()

  while not game.is_over():
    # print(chr(27) + "[2J")
    print_board(game.board)
    if game.next_player == Player.GREEN:
      human_point = input('-- ')
      point = point_from_coords(human_point.strip())
      square = game.board.get_key_by_point(point)
      human_move = input('direction(w/a/s/d)-- ')
      match human_move:
        case 'w': direction = 'top'
        case 'a': direction = 'left'
        case 's': direction = 'bot'
        case 'd': direction = 'right'
      move = jungleBoard.Move.play(square, direction)
    else:
      move = bot.select_move(game)
    print(chr(27) + "[2J")
    print_move(game.next_player, move)
    print()
    game = game.apply_move(move)
  
  print(("green" if game.next_player == Player.RED else "red") + " win")

if __name__ == '__main__':
  main()