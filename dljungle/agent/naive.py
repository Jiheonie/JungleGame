import random
from dljungle.agent.base import Agent
from dljungle.agent.helpers import is_move_valid, home_is_safe
from dljungle.jungleBoard import Move
from dljungle.jungleTypes import Player, Point, Square

class RandomBot(Agent):  
  def find_winning_move(self, game_state):
    if len(game_state.winning_moves) > 0:
      return random.choice(game_state.winning_moves)
    return None
  
  def eliminate_losing_moves(self, game_state):
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


  def find_two_step_win(self, game_state):
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
      good_responses = self.eliminate_losing_moves(next_state)
      if len(good_responses) == 0:
        return candidate
      
    return None


  def select_move(self, game_state):
    winning_move = self.find_winning_move(game_state)
    if winning_move:
      print("win")
      return winning_move
    candidates = self.eliminate_losing_moves(game_state)
    if home_is_safe(game_state):
      dumb_move = "bot" if game_state.next_player == Player.GREEN else "top"
      candidates = list(filter(lambda c: c.direction != dumb_move, candidates))
    if len(candidates) == 0:
      return Move.resign()
    two_step_win = self.find_two_step_win(game_state)
    if two_step_win:
      for c in candidates:
        if c.prev_square.point == two_step_win.prev_square.point and c.direction == two_step_win.direction:
          print("Check: " + str(two_step_win.prev_square.point) + " " + two_step_win.direction)
          return two_step_win
    return random.choice(candidates)
