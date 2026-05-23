import argparse
import os
from datetime import datetime
from tqdm import tqdm
from _common import STRATS
from utils import run_tournament, format_table, save_gif


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--games', type=int, default=2, help='games per pair (split evenly between colors; odd leftover is randomized)')
    p.add_argument('--time', type=float, default=0.5)
    p.add_argument('--strategies', nargs='+', default=list(STRATS), choices=list(STRATS))
    args = p.parse_args()

    out_dir = os.path.join('out', 'tournaments', datetime.now().strftime('%Y%m%d_%H%M%S'))
    gifs_dir = os.path.join(out_dir, 'gifs')
    os.makedirs(gifs_dir, exist_ok=True)

    strategies = [STRATS[name]() for name in args.strategies]
    scores, games = run_tournament(strategies, args.games, args.time)

    table = format_table(strategies, scores)
    with open(os.path.join(out_dir, 'table.txt'), 'w') as f:
        f.write(table + '\n')

    for x_name, o_name, k, history in tqdm(games, desc='saving gifs'):
        save_gif(history, os.path.join(gifs_dir, f'{x_name}_vs_{o_name}_g{k}.gif'))

    print(out_dir)


if __name__ == '__main__':
    main()
