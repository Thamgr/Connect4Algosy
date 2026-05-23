import argparse
from _common import STRATS
from enviroment import Board


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--strategy', default='bf_ab', choices=list(STRATS))
    p.add_argument('--moves', default='', help='comma-separated columns played from start')
    p.add_argument('--time', type=float, default=1.0)
    args = p.parse_args()

    board = Board()
    if args.moves:
        for c in args.moves.split(','):
            board.make_move(int(c))

    print(board)
    print(f'\nTo move: {"X" if board.player == 1 else "O"}')

    strat = STRATS[args.strategy]()
    scores = strat.evaluate(board, args.time)
    print(f'\nStrategy: {strat.name}')
    print('Scores per column (higher = better for side to move):')
    for c in sorted(scores, key=scores.get, reverse=True):
        print(f'  col {c}: {scores[c]}')


if __name__ == '__main__':
    main()
