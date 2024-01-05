import random
from dljungle.agent.base import Agent
from dljungle.agent.helpers import is_move_valid
from dljungle.jungleBoard import Move

class RandomBot(Agent):
  def get_legal_moves(self, game_state):
    keys_lst = list(game_state.board.get_grid().keys())
    directions_lst = ["bot", "top", "left", "right"]
    candidates = []
    for square in keys_lst:
      for direction in directions_lst:
        candidate = [square, direction]
        if is_move_valid(game_state.next_player, game_state.board, square, direction):
          candidates.append(Move.play(candidate[0], candidate[1]))
    return candidates
  
  def find_winning_move(self, game_state):
    for candidate in self.get_legal_moves(game_state):
      next_state = game_state.apply_move(candidate)
      if next_state.is_over() and next_state.winner == game_state.next_player:
        return candidate
    return None
  
  def eliminate_losing_moves(self, game_state):
    possible_moves = []
    for candidate in self.get_legal_moves(game_state):
      next_state = game_state.apply_move(candidate)
      opponent_winning_move = self.find_winning_move(next_state)
      if opponent_winning_move is None:
        possible_moves.append(candidate)
    return possible_moves

  def select_move(self, game_state):
    candidates = self.eliminate_losing_moves(game_state)
    if len(candidates) == 0:
      return Move.resign()
    if self.find_winning_move(game_state):
      chosen_candidate = self.find_winning_move(game_state)
    else:
      chosen_candidate = random.choice(candidates)
    return chosen_candidate
