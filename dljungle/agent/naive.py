import random
from dljungle.agent.base import Agent
from dljungle.agent.helpers import is_move_valid
from dljungle.jungleBoard import Move

class RandomBot(Agent):  
  def find_winning_move(self, game_state):
    for candidate in game_state.legal_moves:
      next_state = game_state.apply_move(candidate)
      if next_state.is_over() and next_state.winner == game_state.next_player:
        return candidate
    return None
  
  def eliminate_losing_moves(self, game_state):
    possible_moves = []
    for candidate in game_state.legal_moves:
      next_state = game_state.apply_move(candidate)
      opponent_winning_move = self.find_winning_move(next_state)
      if opponent_winning_move is None:
        possible_moves.append(candidate)
    return possible_moves

  def find_two_step_win(self, game_state):
    for candidate in game_state.legal_moves:
      next_state = game_state.apply_move(candidate)
      good_responses = self.eliminate_losing_moves(next_state)
      if len(good_responses) == 0:
        return candidate
    return None

  def select_move(self, game_state):
    if self.find_winning_move(game_state):
      print(0)
      return self.find_winning_move(game_state)
    candidates = self.eliminate_losing_moves(game_state)
    if len(candidates) == 0:
      print(1)
      return Move.resign()
    two_step_win = self.find_two_step_win(game_state)
    if two_step_win and two_step_win in candidates:
      print(2)
      print(two_step_win)
      return two_step_win
    print(3)
    return random.choice(candidates)
