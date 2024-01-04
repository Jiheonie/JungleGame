from dljungle.jungleTypes import Square, Point, ChessType, Area

def is_move_valid(player, board, prev_square, direction):
  # correct chessman
  chessman = board.get_chess_by_square(prev_square)
  if not chessman:
    return False
  if chessman.player != player: 
    return False
  # not move out of board
  if prev_square.point.row == 9 and direction == "top":
    return False
  if prev_square.point.row == 1 and direction == "bot":
    return False
  if prev_square.point.col == 7 and direction == "right":
    return False
  if prev_square.point.col == 1 and direction == "left":
    return False
  # not self-capture
  dest_square = board.get_dest_square(prev_square, direction)
  dest_chessman = board.get_chess_by_square(dest_square)
  if dest_chessman:
    if dest_chessman.player == player:
      return False
    # can't catch higher power
    dest_power = dest_chessman.chesstype.value if hasattr(dest_chessman.chesstype, 'value') else 0
    prev_power = chessman.chesstype.value if hasattr(chessman.chesstype, 'value') else 0
    if dest_power == 8 and prev_power == 1:
      return True
    if dest_power > prev_power:
      return False
  # not move in river
  if dest_square.area == Area.RIVER:
    if chessman not in [ChessType.RAT, ChessType.TIGER, ChessType.LION]:
      return False
    if chessman != ChessType.RAT and dest_chessman:
      return False
  # can't move to own cave
  if dest_square.area == Area.CAVE and dest_square.player == player:
    return False


  return True