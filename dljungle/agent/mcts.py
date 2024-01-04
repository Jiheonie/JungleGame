import random
from dljungle.agent.base import Agent
from dljungle.agent.helpers import is_move_valid
from dljungle.jungleBoard import Move

class RandomBot(Agent):
  def select_move(self, game_state):
    keys_lst = list(game_state.board.get_grid().keys())
    directions_lst = ["bot", "top", "left", "right"]

    candidates = []
    for square in keys_lst:
      for direction in directions_lst:
        candidate = [square, direction]
        if is_move_valid(game_state.next_player, game_state.board, square, direction):
          candidates.append(candidate)

    chosen_candidate = random.choice(candidates)
    return Move.play(chosen_candidate[0], chosen_candidate[1])
