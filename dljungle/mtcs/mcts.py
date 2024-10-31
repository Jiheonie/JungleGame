from dljungle.jungleTypes import Player, Square, Point
from dljungle.jungleBoard import Move
from dljungle.agent.base import Agent
from dljungle.agent.naive import RandomBot
from dljungle.utils import print_board, print_move
from dljungle.agent.helpers import home_is_safe, is_move_valid
import random
import math

__all__ = [
  'MCTSAgent',
]

def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
  exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
  return win_pct + temperature * exploration

def find_winning_move(game_state):
    if len(game_state.winning_moves) > 0:
      return random.choice(game_state.winning_moves)
    return None
  
def eliminate_losing_moves(game_state):
  is_checkmate = False

  if game_state.next_player == Player.GREEN:
    trap1 = game_state.board.get_chess_by_point(Point(1, 3))
    trap2 = game_state.board.get_chess_by_point(Point(1, 5))
    trap3 = game_state.board.get_chess_by_point(Point(2, 4))

    possible_moves = []

    if trap1 and trap1.player == Player.RED:
      is_checkmate = True
      trap1_top = game_state.board.get_chess_by_point(Point(2, 3))
      if trap1_top and trap1_top.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(2, 3)), "bot"))
      trap1_left = game_state.board.get_chess_by_point(Point(1, 2))
      if trap1_left and trap1_left.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(1, 2)), "right"))
    
    if trap2 and trap2.player == Player.RED:
      is_checkmate = True
      trap2_top = game_state.board.get_chess_by_point(Point(2, 5))
      if trap2_top and trap2_top.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(2, 5)), "bot"))
      trap2_right = game_state.board.get_chess_by_point(Point(1, 6))
      if trap2_right and trap2_right.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(1, 6)), "left"))
    
    if trap3 and trap3.player == Player.RED:
      is_checkmate = True
      trap3_top = game_state.board.get_chess_by_point(Point(3, 4))
      if trap3_top and trap3_top.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(3, 4)), "bot"))
      trap3_right = game_state.board.get_chess_by_point(Point(2, 5))
      if trap3_right and trap3_right.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(2, 5)), "left"))
      trap3_left = game_state.board.get_chess_by_point(Point(2, 3))
      if trap3_left and trap3_left.player == Player.GREEN:
        possible_moves.append(Move.play(Square.get_by_point(Point(2, 3)), "right"))

    if is_checkmate:
      return possible_moves
  
  if game_state.next_player == Player.RED:
    trap1 = game_state.board.get_chess_by_point(Point(9, 3))
    trap2 = game_state.board.get_chess_by_point(Point(9, 5))
    trap3 = game_state.board.get_chess_by_point(Point(8, 4))

    possible_moves = []

    if trap1 and trap1.player == Player.GREEN:
      is_checkmate = True
      trap1_bot = game_state.board.get_chess_by_point(Point(8, 3))
      if trap1_bot and trap1_bot.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(8, 3)), "top"))
      trap1_left = game_state.board.get_chess_by_point(Point(9, 2))
      if trap1_left and trap1_left.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(9, 2)), "right"))
    
    if trap2 and trap2.player == Player.GREEN:
      is_checkmate = True
      trap2_bot = game_state.board.get_chess_by_point(Point(8, 5))
      if trap2_bot and trap2_bot.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(8, 5)), "top"))
      trap2_right = game_state.board.get_chess_by_point(Point(9, 6))
      if trap2_right and trap2_right.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(9, 6)), "left"))
    
    if trap3 and trap3.player == Player.GREEN:
      is_checkmate = True
      trap3_bot = game_state.board.get_chess_by_point(Point(7, 4))
      if trap3_bot and trap3_bot.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(7, 4)), "top"))
      trap3_right = game_state.board.get_chess_by_point(Point(8, 5))
      if trap3_right and trap3_right.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(8, 5)), "left"))
      trap3_left = game_state.board.get_chess_by_point(Point(8, 3))
      if trap3_left and trap3_left.player == Player.RED:
        possible_moves.append(Move.play(Square.get_by_point(Point(8, 3)), "right"))
        
    if is_checkmate:
      return possible_moves

  return game_state.legal_moves


def find_two_step_win(game_state):
  check_moves = []

  if game_state.next_player == Player.RED:
    chess12 = game_state.board.get_chess_by_point(Point(1, 2))
    chess23 = game_state.board.get_chess_by_point(Point(2, 3))
    chess34 = game_state.board.get_chess_by_point(Point(3, 4))
    chess25 = game_state.board.get_chess_by_point(Point(2, 5))
    chess16 = game_state.board.get_chess_by_point(Point(1, 6))

    if chess12 and chess12.player == Player.RED:
      check_moves.append(Move.play(Square.get_by_point(Point(1, 2)), "right"))
    if chess23 and chess23.player == Player.RED:
      check_moves.append(Move.play(Square.get_by_point(Point(2, 3)), "right"))
      check_moves.append(Move.play(Square.get_by_point(Point(2, 3)), "bot"))
    if chess34 and chess34.player == Player.RED:
      check_moves.append(Move.play(Square.get_by_point(Point(3, 4)), "bot"))
    if chess25 and chess25.player == Player.RED:
      check_moves.append(Move.play(Square.get_by_point(Point(2, 5)), "left"))
      check_moves.append(Move.play(Square.get_by_point(Point(2, 5)), "bot"))
    if chess16 and chess16.player == Player.RED:
      check_moves.append(Move.play(Square.get_by_point(Point(1, 6)), "left"))

  if game_state.next_player == Player.GREEN:
    chess92 = game_state.board.get_chess_by_point(Point(9, 2))
    chess83 = game_state.board.get_chess_by_point(Point(8, 3))
    chess74 = game_state.board.get_chess_by_point(Point(7, 4))
    chess85 = game_state.board.get_chess_by_point(Point(8, 5))
    chess96 = game_state.board.get_chess_by_point(Point(9, 6))

    if chess92 and chess92.player == Player.GREEN:
      check_moves.append(Move.play(Square.get_by_point(Point(9, 2)), "right"))
    if chess83 and chess83.player == Player.GREEN:
      check_moves.append(Move.play(Square.get_by_point(Point(8, 3)), "right"))
      check_moves.append(Move.play(Square.get_by_point(Point(8, 3)), "top"))
    if chess74 and chess74.player == Player.GREEN:
      check_moves.append(Move.play(Square.get_by_point(Point(7, 4)), "top"))
    if chess85 and chess85.player == Player.GREEN:
      check_moves.append(Move.play(Square.get_by_point(Point(8, 5)), "left"))
      check_moves.append(Move.play(Square.get_by_point(Point(8, 5)), "top"))
    if chess96 and chess96.player == Player.GREEN:
      check_moves.append(Move.play(Square.get_by_point(Point(9, 6)), "left"))

  for candidate in check_moves:
    if not is_move_valid(game_state.next_player, game_state.board, candidate.prev_square, candidate.direction):
      continue
    next_state = game_state.apply_move(candidate)
    good_responses = eliminate_losing_moves(next_state)
    if len(good_responses) == 0:
      return candidate
    
  return None


def get_good_moves(game_state):
  winning_move = find_winning_move(game_state)
  if winning_move:
    print("win")
    return [winning_move]
  candidates = eliminate_losing_moves(game_state)
  if home_is_safe(game_state):
    dumb_move = "bot" if game_state.next_player == Player.GREEN else "top"
    candidates = list(filter(lambda c: c.direction != dumb_move, candidates))
  if len(candidates) == 0:
    return [Move.resign()]
  two_step_win = find_two_step_win(game_state)
  if two_step_win:
    for c in candidates:
      if c.prev_square.point == two_step_win.prev_square.point and c.direction == two_step_win.direction:
        print("Check: " + str(two_step_win.prev_square.point) + " " + two_step_win.direction)
        return [two_step_win]
  return candidates

# def get_good_moves(game_state):
#   if home_is_safe(game_state):
#     dumb_move = "bot" if game_state.next_player == Player.GREEN else "top"
#     return list(filter(lambda c: c.direction != dumb_move, game_state.legal_moves))
#   return game_state.legal_moves

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
      if (m.prev_square):
        print('%s go %s - %.3f (%d)' % (m.prev_square.point, m.direction, s, n))
      else:
        print('resign')

    best_move = None
    best_pct = -1.0
    for child in root.children:
      child_pct = child.winning_frac(game_state.next_player)
      if child_pct > best_pct:
        best_pct = child_pct
        best_move = child.move
    if best_move.prev_square:
      print('Select move at %s go %s with win pct %3f' % (best_move.prev_square.point, best_move.direction, best_pct))
      return best_move
    
    return Move.resign()
  
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
      
    if not best_child:
      print("Number of child: " + str(len(node.unvisited_moves)))
      print(f"Can add child? {node.can_add_child()}")
      print(f"Is Terminal? {node.is_terminal()}")
      print("Best Score: " + str(best_score))
      print(node.game_state.next_player)
      print_board(node.game_state.board)

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