import copy
from dljungle.jungleTypes import Player, ChessType, Area, Square
from dljungle.agent.helpers import is_move_valid, is_winning_move

class Move():
  def __init__(self, prev_square=None, direction=None, is_resign=False):
    assert ((prev_square is not None) & (direction is not None)) ^ is_resign
    self.prev_square = prev_square
    self.direction = direction
    self.is_play = (self.prev_square is not None)
    self.is_resign = is_resign

  @classmethod
  def play(cls, prev_square, direction):
    return Move(prev_square=prev_square, direction=direction)
  
  @classmethod
  def resign(cls):
    return Move(is_resign=True)

  def __eq__(self, other):
    if isinstance(other, Move):
      return self.__dict__ == other.__dict__
    return False
  

class Board():
  def __init__(self):
    self.num_rows = 9
    self.num_cols = 7
    self._grid = {} # square:chessman
    self.is_over = False

  def get_grid(self):
    return self._grid

  def add_square(self, square, chessman=None):
    self._grid[square] = chessman

  def is_on_grid(self, point):
    return 1 <= point.row <= self.num_rows and \
      1 <= point.col <= self.num_cols

  def get_key_by_point(self, point):
    for key in self._grid:
      if key.point == point:
        return key
    return None

  def get_chess_by_point(self, point):
    square = self.get_key_by_point(point)
    return self._grid.get(square)
  
  def get_chess_by_square(self, prev_square_raw):
    prev_square = self.get_key_by_point(prev_square_raw.point)
    return self._grid.get(prev_square)
  
  def get_dest_square(self, prev_square_raw, direction):
    prev_square = self.get_key_by_point(prev_square_raw.point)
    dest_point = prev_square.point.neighbors()[direction]
    for key in self._grid:
      if key.point == dest_point:
        return key
    return None

  def place_chessman(self, player, prev_square, direction):
    chessman = self.get_chess_by_square(prev_square)
    assert (chessman is not None), "no chessman in square"

    dest_square = self.get_dest_square(prev_square, direction)
    assert (dest_square is not None), "out of board"

    assert player == chessman.player, "not your chessman"

    if dest_square.area == Area.RIVER:
      assert chessman.chesstype in [ChessType.RAT, ChessType.LION, ChessType.TIGER], \
        "can't move in river"
      if chessman.chesstype in [ChessType.LION, ChessType.TIGER]:
        while dest_square.area == Area.RIVER:
          assert self._grid.get(dest_square) is None, "blocked, can't jump"
          dest_square = Square.get_by_point(dest_square.point[direction])

    if dest_square.area == Area.CAVE: 
      assert chessman.player != dest_square.player, \
        "can't move to own cave"
      self.is_over = True

    placed_chessman = self._grid.get(dest_square)
    if placed_chessman:
      assert placed_chessman.player != player, "ally has already been here"
      dest_power = placed_chessman.chesstype.value if hasattr(placed_chessman.chesstype, 'value') else 0
      prev_power = chessman.chesstype.value if hasattr(chessman.chesstype, 'value') else 0
      assert (dest_power <= prev_power) ^ (dest_power == 8 and prev_power == 1), "can't catch"

    if prev_square.area == Area.TRAP and chessman.player != prev_square.player:
      chessman.chesstype = chessman.lost_power

    if dest_square.area == Area.TRAP and chessman.player != dest_square.player:
      chessman.chesstype = 0  

    self.move_chessman(chessman, self.get_key_by_point(prev_square.point), dest_square)

  def move_chessman(self, chessman, prev_square, dest_square):
    self._grid[dest_square] = chessman
    self._grid[prev_square] = None
  
  def get_checkmate(self):
    for square in self._grid:
      if square.area == Area.TRAP:
        chessman = self.get_chess_by_square(square)
        if chessman.player != square.player:
          return square
    return None

  
class GameState():
  def __init__(self, board, next_player, previous, move):
    self.board = board
    self.next_player = next_player
    self.previous_state = previous
    self.last_move = move
    self.winner = None
    self.winning_moves = []
    self.legal_moves = self.get_legal_moves()

  def __eq__(self, __value: object) -> bool:
    return self.__dict__ == __value.__dict__

  def apply_move(self, move):
    # print(0)
    if move.is_play:
      next_board = copy.deepcopy(self.board)
      next_board.place_chessman(self.next_player, move.prev_square, move.direction)
    else:
      next_board = self.board
    # print(1)
    return GameState(next_board, self.next_player.other, self, move)

  def get_legal_moves(self):
    keys_lst = list(self.board.get_grid().keys())
    directions_lst = ["bot", "top", "left", "right"]
    candidates = []
    for square in keys_lst:
      for direction in directions_lst:
        candidate = [square, direction]
        if is_move_valid(self.next_player, self.board, square, direction):
          candidates.append(Move.play(candidate[0], candidate[1]))
          if is_winning_move(self, candidate[0], candidate[1]):
            self.winning_moves.append(Move.play(candidate[0], candidate[1]))
    return candidates
  
  @classmethod
  def new_game(cls, board):
    return GameState(board, Player.GREEN, None, None)
  
  def is_over(self):
    if self.last_move is None:
      return False
    if self.last_move.is_resign:
      self.winner = self.next_player  
      return True
    second_last_move = self.previous_state.last_move
    if second_last_move is None:
      return False
    if self.board.is_over:
      self.winner = self.next_player.other
      return True
    return False