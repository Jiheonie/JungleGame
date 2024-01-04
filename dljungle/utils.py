from dljungle import jungleTypes
from dljungle.jungleTypes import Square


COLS = 'ABCDEFG'
CHESS_TO_CHAR = {
  jungleTypes.Player.GREEN: 'G ',
  jungleTypes.Player.RED: 'R ',
}

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
        line.append(' __ ')
      else: 
        chess_power = chessman.chesstype.value if hasattr(chessman.chesstype, 'value') else 0
        line.append(f" {chess_power}{CHESS_TO_CHAR[chessman.player]}")
    print(f"{bump}{row}  {''.join(line)}")
  print()
  print('     ' + '   '.join(COLS[:board.num_cols]))
