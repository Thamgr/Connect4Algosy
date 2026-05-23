import random
from tqdm import tqdm
from .play import play_game


def run_tournament(strategies, games_per_pair=2, time_limit=1.0):
    n = len(strategies)
    scores = [[0.0] * n for _ in range(n)]
    assignments = []
    half = games_per_pair // 2
    for i in range(n):
        for j in range(i + 1, n):
            slots = [(i, j)] * half + [(j, i)] * half
            if games_per_pair % 2:
                slots.append(random.choice([(i, j), (j, i)]))
            assignments.extend(slots)

    games = []
    counts = {}
    for x_idx, o_idx in tqdm(assignments, desc='tournament'):
        winner, history = play_game(strategies[x_idx], strategies[o_idx], time_limit)
        if winner == 1:
            scores[x_idx][o_idx] += 1
        elif winner == -1:
            scores[o_idx][x_idx] += 1
        else:
            scores[x_idx][o_idx] += 0.5
            scores[o_idx][x_idx] += 0.5
        key = (x_idx, o_idx)
        k = counts.get(key, 0)
        counts[key] = k + 1
        games.append((strategies[x_idx].name, strategies[o_idx].name, k, history))
    return scores, games


def format_table(strategies, scores):
    names = [s.name for s in strategies]
    n = len(names)
    w = max(max(len(name) for name in names) + 2, 10)
    lines = []
    header = ' ' * w + ''.join(f'{name:>{w}}' for name in names) + f'{"total":>{w}}'
    lines.append(header)
    for i in range(n):
        total = sum(scores[i])
        row = f'{names[i]:>{w}}'
        for j in range(n):
            cell = '—' if i == j else f'{scores[i][j]:g}'
            row += f'{cell:>{w}}'
        row += f'{total:g}'.rjust(w)
        lines.append(row)
    return '\n'.join(lines)
