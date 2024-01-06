from dljungle.jungleTypes import GameResult
from dljungle.agent.base import Agent
import random

def reverse_game_result(game_result):
  if game_result == GameResult.LOSS:
    return game_result.WIN
  return game_result.WIN

def best_result(game_state):
  if game_state.is_over():
    if game_state.winner == game_state.next_player:
      return GameResult.WIN
    return GameResult.LOSS
  best_result_so_far = GameResult.LOSS
  for candidate in game_state.legal_moves:
    next_state = game_state.apply_move(candidate)
    opponent_best_result = best_result(next_state)
    our_result = reverse_game_result(opponent_best_result)
    if our_result.value > best_result_so_far.value:
      best_result_so_far = our_result
  return best_result_so_far

class MinimaxAgent(Agent):
  def select_move(self, game_state):
    winning_moves = []
    losing_moves = []
    for candidate in game_state.legal_moves:
      next_state = game_state.apply_move(candidate)
      opponent_best_outcome = best_result(next_state)
      our_best_outcome = reverse_game_result(opponent_best_outcome)
      if our_best_outcome == GameResult.WIN:
        winning_moves.append(candidate)
      else:
        losing_moves.append(candidate)
    if winning_moves:
      return random.choice(winning_moves)
    return random.choice(losing_moves)