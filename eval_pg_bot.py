import argparse

import h5py

from dljungle.jungleBoard import GameState, Board
from dljungle.jungleTypes import Player
from dljungle.utils import print_board, custom_board
from dljungle.agent.pg import load_policy_agent


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

  while not game.is_over():
    next_move = agents[game.next_player].select_move(game)
    moves.append(next_move)
    game = game.apply_move(next_move)

  print_board(board=board)

  return game.winner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent1', required=True)
    parser.add_argument('--agent2', required=True)
    parser.add_argument('--num-games', '-n', type=int, default=10)

    args = parser.parse_args()

    agent1 = load_policy_agent(h5py.File(args.agent1))
    agent2 = load_policy_agent(h5py.File(args.agent2))

    wins = 0
    losses = 0
    color1 = Player.GREEN
    for i in range(args.num_games):
        print('Simulating game %d/%d...' % (i + 1, args.num_games))
        if color1 == Player.GREEN:
            gp, rp = agent1, agent2
        else:
            rp, gp = agent1, agent2
        winner = simulate_game(gp, rp)
        if winner == color1:
            wins += 1
        else:
            losses += 1
        color1 = color1.other
    print('Agent 1 record: %d/%d' % (wins, wins + losses))


if __name__ == '__main__':
    main()