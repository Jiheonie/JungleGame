from enum import Enum
from collections import namedtuple


class Player(Enum):
  GREEN = 1
  RED = 2

  @property
  def other(self):
    return Player.GREEN if self == Player.RED else Player.RED


class Area(Enum):
  CAVE = 1
  TRAP = 2
  RIVER = 3
  GROUND = 4


class ChessType(Enum):
  ELEPHANT = 8
  LION = 7
  TIGER = 6
  LEOPARD = 5
  DOG = 4
  WOLF = 3
  CAT = 2
  RAT = 1


class Point(namedtuple('Point', 'row col')):
  def neighbors(self):
    return {
      "bot": Point(self.row - 1, self.col),
      "top": Point(self.row + 1, self.col),
      "left": Point(self.row, self.col - 1),
      "right": Point(self.row, self.col + 1),
    }
  
  def __eq__(self, other) -> bool:
    if isinstance(other, Point):
      return self.row == other.row and self.col == other.col
    return False
  

class Square():
  lst = []

  def __init__(self, point, player=0, area=Area.GROUND):
    self.point = point
    self.player = player
    self.area = area
    Square.lst.append(self)

  @classmethod
  def get_lst(cls):
    return cls.lst

  @classmethod
  def get_by_point(cls, point):
    for item in cls.lst:
      if point == item.point:
        return item
    return None

  @classmethod
  def get_dest_square(cls, prev_square, direction):
    return cls.get_by_point(prev_square.point.neighbors()[direction])

  def set_area(self, player, area):
    self.player = player
    self.area = area


class ChessMan():
  def __init__(self, player, chesstype):
    self.player = player
    self.chesstype = chesstype
    self.lost_power = chesstype


class GameResult(Enum):
  LOSS = 0
  WIN = 1