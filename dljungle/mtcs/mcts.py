from dljungle.jungleTypes import Player
from dljungle.agent.base import Agent
from dljungle.agent.naive import RandomBot
from dljungle.utils import print_board, print_move
from dljungle.agent.helpers import home_is_safe
import random
import math

__all__ = [
  'MCTSAgent',
]

def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
  exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
  return win_pct + temperature * exploration

def get_good_moves(game_state):
  if home_is_safe(game_state):
    dumb_move = "bot" if game_state.next_player == Player.GREEN else "top"
    return list(filter(lambda c: c.direction != dumb_move, game_state.legal_moves))
  return game_state.legal_moves

class MCTSNode:
  def __init__(self, game_state, parent=None, move=None):
    self.game_state = game_state
    self.parent = parent
    self.move = move
    self.children = []
    self.win_counts = {
      Player.GREEN: 0,
      Player.RED: 0
    }
    self.num_rollouts = 0
    self.unvisited_moves = get_good_moves(game_state)

  def add_random_child(self):
    index = random.randint(0, len(self.unvisited_moves) - 1)
    new_move = self.unvisited_moves.pop(index)
    print("Unvisited Move: " + str(len(self.unvisited_moves)))
    new_game_state = self.game_state.apply_move(new_move)
    new_node = MCTSNode(new_game_state, self, new_move)
    self.children.append(new_node)
    return new_node

  def record_win(self, winner):
    self.win_counts[winner] += 1
    self.num_rollouts += 1

  def can_add_child(self):
    return len(self.unvisited_moves) > 0
  
  def is_terminal(self):
    return self.game_state.is_over()
  
  def winning_frac(self, player):
    return float(self.win_counts[player]) / float(self.num_rollouts)


class MCTSAgent(Agent):
  def __init__(self, num_rounds, temperature):
    Agent.__init__(self)
    self.num_rounds = num_rounds
    self.temperature = temperature

  def select_move(self, game_state):
    root = MCTSNode(game_state)

    for i in range(self.num_rounds):
      print(f'Round: {i}')
      node = root
      while (not node.can_add_child()) and (not node.is_terminal()):
        node = self.select_child(node)

      if node.can_add_child():
        node = node.add_random_child()

      # simulate full game trên node này luôn sao? 
      winner = self.simulate_random_game(node.game_state)

      while node is not None:
        node.record_win(winner)
        node = node.parent

    scored_moves = [
      (child.winning_frac(game_state.next_player), child.move, child.num_rollouts)
      for child in root.children
    ]
    scored_moves.sort(key=lambda x: x[0], reverse=True)
    for s, m, n in scored_moves[:10]:
      print('%s go %s - %.3f (%d)' % (m.prev_square.point, m.direction, s, n))

    best_move = None
    best_pct = -1.0
    for child in root.children:
      child_pct = child.winning_frac(game_state.next_player)
      if child_pct > best_pct:
        best_pct = child_pct
        best_move = child.move
    print('Select move at %s go %s with win pct %3f' % (best_move.prev_square.point, best_move.direction, best_pct))
    return best_move
  
  def select_child(self, node):
    total_rollouts = sum(child.num_rollouts for child in node.children)
    best_score = -1
    best_child = None
    for child in node.children:
      score = uct_score(
        total_rollouts, 
        child.num_rollouts, 
        child.winning_frac(node.game_state.next_player),
        self.temperature
      )
      if score > best_score:
        best_score = score
        best_child = child

    return best_child
  
  @staticmethod
  def simulate_random_game(game):
    bots = {
      Player.GREEN: RandomBot(),
      Player.RED: RandomBot()
    }
    while not game.is_over():
      bot_move = bots[game.next_player].select_move(game)
      game = game.apply_move(bot_move)
    return game.winner