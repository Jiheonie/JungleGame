from dljungle.jungleTypes import Point, Player
from dljungle.agent.base import Agent
import random

MAX_SCORE = 99999
MIN_SCORE = -99999

def alpha_beta_result(game_state, max_depth, best_green, best_red, eval_fn):
  if game_state.is_over():
    if game_state.winner == game_state.next_player:
      return MAX_SCORE
    return MIN_SCORE
  
  if max_depth == 0:
    return eval_fn(game_state)

  best_so_far = MIN_SCORE

  for candidate in game_state.legal_moves:
    next_state = game_state.apply_move(candidate)
    opponent_best_result = alpha_beta_result(
      next_state, max_depth - 1,
      best_green, best_red,
      eval_fn
    )
    our_result = -1 * opponent_best_result

  if our_result > best_so_far:
    best_so_far = our_result

  if game_state.next_player == Player.RED:
    if best_so_far > best_red:
      best_red = best_so_far
    outcome_for_green = -1 * best_so_far
    if outcome_for_green < best_green:
      return best_so_far
    
  elif game_state.next_player == Player.GREEN:
    if best_so_far > best_green:
      best_green = best_so_far
    outcome_for_red = -1 * best_so_far
    if outcome_for_red < best_red:
      return best_so_far
    
  return best_so_far


class AlphaBetaAgent(Agent):
  def __init__(self, max_depth, eval_fn):
    super().__init__()
    self.max_depth = max_depth
    self.eval_fn = eval_fn

  def select_move(self, game_state):
    best_moves = []
    best_score = None
    best_green = MIN_SCORE
    best_red = MIN_SCORE

    for candidate in game_state.legal_moves:
      next_state = game_state.apply_move(candidate)
      opponent_best_outcome = alpha_beta_result(
        next_state, self.max_depth,
        best_green, best_red,
        self.eval_fn
      )
      our_best_outcome = -1 * opponent_best_outcome
      if (not best_moves) or our_best_outcome > best_score:
        best_moves = [candidate]
        best_score = our_best_outcome
        if game_state.next_player == Player.GREEN:
          best_green = best_score
        elif game_state.next_player == Player.RED:
          best_red = best_score
      elif our_best_outcome == best_score:
        best_moves.append(candidate)

    return random.choice(best_moves)