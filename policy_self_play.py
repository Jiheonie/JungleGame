import argparse
import datetime

import h5py
from dljungle.rl.experience import ExperienceCollector, combine_experience
from dljungle.jungleBoard import GameState, Board
from dljungle.jungleTypes import Player, Square, Point
from dljungle.utils import custom_board, print_board
from dljungle.agent.pg import load_policy_agent

def capture_diff(game_state):
  gp = 0
  rp = 0
  for r in range(1, 10):
    for c in range(1, 8):
      chess = game_state.board.get_chess_by_point(Point(r, c))
      if chess:
        if chess.player == Player.GREEN:
          gp += 1
        else:
          rp += 1
  diff = gp - rp
  if diff >= 0:
    return Player.GREEN
  return Player.RED

def simulate_game(green, red):
  moves = []

  board = Board()
  custom_board(board=board)
  print_board(board=board)
  game = GameState.new_game(board=board)
  agents = {
    Player.GREEN: green,
    Player.RED: red
  }

  num_moves = 0

  while not game.is_over() and num_moves < 100:
    next_move = agents[game.next_player].select_move(game)
    moves.append(next_move)
    game = game.apply_move(next_move)
    num_moves += 1

  print_board(board=board)

  if num_moves == 100:
    return capture_diff(game_state=game)

  return game.winner


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--learning-agent', required=True)
  parser.add_argument('--num-games', type=int, default=10)
  parser.add_argument('--experience-out', required=True)

  args = parser.parse_args()
  agent_filename = args.learning_agent
  experience_filename = args.experience_out
  num_games = args.num_games

  agent1 = load_policy_agent(h5py.File(agent_filename))
  agent2 = load_policy_agent(h5py.File(agent_filename))
  collector1 = ExperienceCollector()
  collector2 = ExperienceCollector()
  agent1.set_collector(collector1)
  agent2.set_collector(collector2)

  for i in range(args.num_games):
    print('Simulating game %d/%d...' % (i + 1, args.num_games))
    collector1.begin_episode()
    collector2.begin_episode()

    winner = simulate_game(agent1, agent2)
    if winner == Player.GREEN:
      collector1.complete_episode(reward=1)
      collector2.complete_episode(reward=-1)
    else:
      collector2.complete_episode(reward=1)
      collector1.complete_episode(reward=-1)

  experience = combine_experience([collector1, collector2])
  with h5py.File(experience_filename, 'w') as experience_outf:
    experience.serialize(experience_outf)


if __name__ == '__main__':
  main()