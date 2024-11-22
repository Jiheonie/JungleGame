import numpy as np

from dljungle.encoders.base import Encoder
from dljungle.jungleTypes import Point, Player, ChessType

class OnePlaneEncoder(Encoder):
  def __init__(self):
    self.board_width = 7
    self.board_height = 9
    self.num_planes = 1

  def name(self):
    return 'oneplane'
  
  def encode(self, game_state):
    # 5: area_player, area_type, chessman_player, chessman_type, chessman_lost_power
    # board_matrix = np.zeros((1, 9, 7, 5))
    board_matrix = np.zeros((9, 7, 5))
    next_player = game_state.next_player
    for r in range(self.board_height):
      for c in range(self.board_width):
        square = game_state.board.get_key_by_point(Point(r + 1, c + 1))
        # board_matrix[0, r, c, 0] = square.player.value if isinstance(square.player, Player) else 0
        board_matrix[r, c, 0] = square.player.value if isinstance(square.player, Player) else 0
        # board_matrix[0, r, c, 1] = square.area.value
        board_matrix[r, c, 1] = square.area.value
        chess = game_state.board.get_chess_by_point(Point(r + 1, c + 1))
        if chess == None:
          continue
        # board_matrix[0, r, c, 3] = chess.chesstype.value if isinstance(chess.chesstype, ChessType) else 0
        board_matrix[r, c, 3] = chess.chesstype.value if isinstance(chess.chesstype, ChessType) else 0
        # board_matrix[0, r, c, 4] = chess.lost_power.value
        board_matrix[r, c, 4] = chess.lost_power.value
        if chess.player == next_player:
          # board_matrix[0, r, c, 2] = 1
          board_matrix[r, c, 2] = 1
        else:
          # board_matrix[0, r, c, 2] = -1
          board_matrix[r, c, 2] = -1
    return board_matrix
  
  def encode_point(self, point):
    return self.board_width * (point.row - 1) + (point.col - 1)

  def decode_point_index(self, index):
    direction = index % 4
    if direction == 0:
      dir_str = "top"
    elif direction == 1:
      dir_str = "right"
    elif direction == 2:
      dir_str = "bot"
    else:
      dir_str = "left"
    row_col = index // 4
    row = row_col // self.board_width
    col = row_col % self.board_width
    return Point(row=row+1, col=col+1), dir_str
  
  def encode_moves(self, moves):
    moves_arr = np.zeros((self.board_height * self.board_width * 4), dtype=int)
    for m in moves:
      if m.direction == "top":
        i = 0
      elif m.direction == "right":
        i = 1
      elif m.direction == "bot":
        i = 2
      else:
        i = 3
      idx = self.encode_point(m.prev_square.point) * 4 + i
      moves_arr[idx] = 1
    return moves_arr
    
  def num_points(self):
    return self.board_width * self.board_height
  
  def shape(self):
    return self.num_planes, self.board_height, self.board_width
  
def create():
  return OnePlaneEncoder()