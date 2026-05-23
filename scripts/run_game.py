import argparse
import os
from _common import STRATS
from utils import play_game, save_gif


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--x', default='mcts', choices=list(STRATS))
    p.add_argument('--o', default='random', choices=list(STRATS))
    p.add_argument('--time', type=float, default=1.0)
    p.add_argument('--out', default='game.gif')
    args = p.parse_args()

    sx, so = STRATS[args.x](), STRATS[args.o]()
    winner, history = play_game(sx, so, args.time)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    save_gif(history, args.out)
    result = {1: f'X ({args.x})', -1: f'O ({args.o})', 0: 'draw'}[winner]
    print(f'Winner: {result}; moves: {len(history) - 1}; gif: {args.out}')


if __name__ == '__main__':
    main()
