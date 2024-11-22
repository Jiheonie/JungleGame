import numpy as np
import random
from keras.api.models import Sequential
from keras.api.optimizers import SGD
from dljungle.agent.naive import Agent
from dljungle import kerasutil
from dljungle.jungleTypes import Player, Point, Square
from dljungle.jungleBoard import Move
from dljungle.agent.helpers import home_is_safe, is_move_valid
from dljungle.encoders.base import get_encoder_by_name


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
    return []
  two_step_win = find_two_step_win(game_state)
  if two_step_win:
    for c in candidates:
      if c.prev_square.point == two_step_win.prev_square.point and c.direction == two_step_win.direction:
        print("Check: " + str(two_step_win.prev_square.point) + " " + two_step_win.direction)
        return [two_step_win]
  return candidates

def clip_probs(original_probs):
  min_p = 1e-5
  max_p = 1 - min_p
  clipped_probs = np.clip(original_probs, min_p, max_p)
  clipped_probs = clipped_probs / np.sum(clipped_probs)
  return clipped_probs


def prepare_experience_data(experience):
  experience_size = experience.actions.shape[0]
  target_vectors = np.zeros((experience_size, 9 * 7 * 4))
  for i in range(experience_size):
    action = experience.actions[i]
    reward = experience.rewards[i]
    target_vectors[i][action] = reward
  return target_vectors


class PolicyAgent(Agent):
  def __init__(self, model, encoder):
    self._model = model
    self._encoder = encoder   
    self._collector = None
    self._temperature = 0.0


  def set_temperature(self, temperature):
    self._temperature = temperature


  def set_collector(self, collector):
    self._collector = collector 


  def serialize(self, h5file):
    h5file.create_group('encoder')
    h5file['encoder'].attrs['name'] = self._encoder.name()
    h5file.create_group('model')
    kerasutil.save_model_to_hdf5_group(self._model, h5file['model'])


  def select_move(self, game_state):
    good_moves = get_good_moves(game_state=game_state)
    if len(good_moves) > 0:
      moves = self._encoder.encode_moves(good_moves)
      # num_moves = len(moves)
      num_moves = 9 * 7 * 4

      board_tensor = self._encoder.encode(game_state)
      X = np.array([board_tensor])

      move_probs = self._model.predict(X)[0]
      move_probs = clip_probs(move_probs)

      candidates = np.arange(num_moves)
      ranked_moves = np.random.choice(candidates, num_moves, replace=False, p=move_probs)
      for point_idx in ranked_moves:
        # print(point_idx)
        # print(moves)
        # print(moves[point_idx])
        point, direction = self._encoder.decode_point_index(point_idx)
        # print(point)
        if moves[point_idx] == 1:
          if self._collector is not None:
            self._collector.record_decision(state=board_tensor, action=point_idx)
          square = Square.get_by_point(point=point)
          return Move.play(prev_square=square, direction=direction)
    return Move.resign()


  def train(self, experience, lr, clipnorm, batch_size):
    self._model.compile(
      loss='categorical_crossentropy',
      optimizer=SGD(learning_rate=lr, clipnorm=clipnorm))
    
    target_vectors = prepare_experience_data(experience=experience)
    self._model.fit(experience.states, target_vectors, batch_size=batch_size, epochs=1)


def load_policy_agent(h5file):
  model = kerasutil.load_model_from_hdf5_group(h5file['model'])
  encoder_name = h5file['encoder'].attrs['name']
  if not isinstance(encoder_name, str):
    encoder_name = encoder_name.decode('ascii')
  encoder = get_encoder_by_name(encoder_name)
  return PolicyAgent(model, encoder)