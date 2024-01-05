from dljungle import jungleTypes
from dljungle.jungleTypes import Player, Area, ChessType, Point, ChessMan
from dljungle.jungleTypes import Square


COLS = 'ABCDEFG'
CHESS_TO_CHAR = {
  jungleTypes.Player.GREEN: 'G ',
  jungleTypes.Player.RED: 'R ',
}

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


# hard code place caves, traps, rivers
def custom_board(board):
  for r in range(1, board.num_rows + 1):
    for c in range(1, board.num_cols + 1):
      square = Square(Point(r, c))
      if (r, c) in SPECIAL_AREA:
        player = SPECIAL_AREA.get((r, c))[0]
        area = SPECIAL_AREA.get((r, c))[1]
        square.set_area(player, area)
      if (r, c) in START_CHESS:
        chess = START_CHESS.get((r, c))
        chessman = ChessMan(chess[0], chess[1])
        board.add_square(square, chessman)
      else:
        board.add_square(square)

def print_move(player, move):
  if move.is_resign: 
    move_str = 'resigns'
  else: 
    dest_square = Square.get_dest_square(move.prev_square, move.direction)
    if dest_square:
      start_col = COLS[move.prev_square.point.col - 1]
      start_row = move.prev_square.point.row
      dest_col = COLS[dest_square.point.col - 1]
      dest_row = dest_square.point.row
      move_str = f'{start_col}{start_row} -> {dest_col}{dest_row}'
    else: 
      move_str = "Invalid move"
  print(f"{player} {move_str}")

def print_board(board):
  for row in range(board.num_rows, 0, -1):
    bump = " " if row <= 9 else ""
    line = []
    for col in range(1, board.num_cols + 1):
      square = board.get_key_by_point(jungleTypes.Point(row=row, col=col))
      chessman = board.get_grid().get(square)
      if chessman is None:
        match square.area:
          case Area.GROUND: 
            line.append(' __ ')
          case Area.CAVE: 
            line.append(' <> ')
          case Area.TRAP: 
            line.append(' xx ')
          case Area.RIVER: 
            line.append(' .. ')
      else: 
        chess_power = chessman.chesstype.value if hasattr(chessman.chesstype, 'value') else 0
        line.append(f" {chess_power}{CHESS_TO_CHAR[chessman.player]}")
    print(f"{bump}{row}  {''.join(line)}")
  print()
  print('     ' + '   '.join(COLS[:board.num_cols]))

def point_from_coords(coords):
  col = COLS.index(coords[0]) + 1
  row = int(coords[1:])
  return jungleTypes.Point(row=row, col=col)