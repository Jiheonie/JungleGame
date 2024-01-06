from dljungle.jungleTypes import Point, Player
from dljungle.agent.base import Agent
import random

MAX_SCORE = 99999
MIN_SCORE = -99999

def capture_diff(game_state):
  green_chess = 0
  red_chess = 0
  for r in range(1, game_state.board.num_rows + 1):
    for c in range(1, game_state.board.num_cols + 1):
      square = game_state.board.get_key_by_point(Point(r, c))
      chessman = game_state.board.get_chess_by_square(square)
      if chessman:
        if chessman.player == Player.GREEN:
          green_chess += chessman.chesstype.value
        elif chessman.player == Player.RED:
          red_chess += chessman.chesstype.value
  diff = green_chess - red_chess
  if game_state.next_player == Player.GREEN:
    return diff
  return -1 * diff

def best_result(game_state, max_depth, eval_fn):
  if game_state.is_over():
    if game_state.winner == game_state.next_player:
      return MAX_SCORE
    return MIN_SCORE
  
  if max_depth == 0:
    return eval_fn(game_state)

  best_result_so_far = MIN_SCORE
  for candidate in game_state.legal_moves:
    next_state = game_state.apply_move(candidate)
    opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
    our_result = -1 * opponent_best_result
    if our_result > best_result_so_far:
      best_result_so_far = our_result
  return best_result_so_far

class DepthPruningAgent(Agent):
  def __init__(self, max_depth, eval_fn):
    super().__init__()
    self.max_depth = max_depth
    self.eval_fn = eval_fn

  def select_move(self, game_state):
    best_moves = []
    best_score = None
    for candidate in game_state.legal_moves:
      next_state = game_state.apply_move(candidate)
      opponent_best_outcome = best_result(next_state, self.max_depth, self.eval_fn)
      our_best_outcome = -1 * opponent_best_outcome
      if (not best_moves) or our_best_outcome > best_score:
        best_moves = [candidate]
        best_score = our_best_outcome
      elif our_best_outcome == best_score:
        best_moves.append(candidate)
    return random.choice(best_moves)