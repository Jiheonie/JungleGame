import numpy as np

from dljungle.encoders.base import Encoder
from dljungle.jungleTypes import Point, Player

class OnePlaneEncoder(Encoder):
  def __init__(self):
    self.board_width = 7
    self.board_height = 9
    self.num_planes = 1

  def name(self):
    return 'oneplane'
  
  def encode(self, game_state):
    # 5: area_player, area_type, chessman_player, chessman_type, chessman_lost_power
    board_matrix = np.zeros((1, 9, 7, 5))
    next_player = game_state.next_player
    for r in range(self.board_height):
      for c in range(self.board_width):
        square = game_state.board.get_key_by_point(Point(r + 1, c + 1))
        board_matrix[0, r, c, 0] = square.player.value if isinstance(square.player, Player) else 0
        board_matrix[0, r, c, 1] = square.area.value
        chess = game_state.board.get_chess_by_point(Point(r + 1, c + 1))
        if chess == None:
          continue
        board_matrix[0, r, c, 3] = chess.chesstype.value
        board_matrix[0, r, c, 4] = chess.lost_power.value
        if chess.player == next_player:
          board_matrix[0, r, c, 2] = 1
        else:
          board_matrix[0, r, c, 2] = -1
    return board_matrix
  
  def encode_point(self, point):
    return self.board_width * (point.row - 1) + (point.col - 1)

  def decode_point_index(self, index):
    row = index // self.board_width
    col = index % self.board_width
    return Point(row=row+1, col=col+1)
  
  def num_points(self):
    return self.board_width * self.board_height
  
  def shape(self):
    return self.num_planes, self.board_height, self.board_width
  
def create():
  return OnePlaneEncoder()