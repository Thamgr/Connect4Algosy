from .board import ROWS, COLS


def _windows(grid):
    for r in range(ROWS):
        for c in range(COLS - 3):
            yield [grid[r][c + i] for i in range(4)]
    for r in range(ROWS - 3):
        for c in range(COLS):
            yield [grid[r + i][c] for i in range(4)]
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            yield [grid[r + i][c + i] for i in range(4)]
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            yield [grid[r - i][c + i] for i in range(4)]


SCORE_BY_COUNT = {2: 2, 3: 4, 4: 100}


def eval_lines(board):
    """Score from board.player's view: each 4-window without opponent pieces grants 2 for 2-in-a-row, 4 for 3, 100 for 4."""
    me = board.player
    other = -me
    return _count_lines(board.grid, me, other) - _count_lines(board.grid, other, me)


def _count_lines(grid, p, other):
    total = 0
    for cells in _windows(grid):
        if other in cells:
            continue
        total += SCORE_BY_COUNT.get(cells.count(p), 0)
    return total


def eval_pairs(board):
    """Simpler variant: +1 for each adjacent same-color pair (8 directions, counted once)."""
    me = board.player
    return _count_pairs(board.grid, me) - _count_pairs(board.grid, -me)


def _count_pairs(grid, p):
    cnt = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != p:
                continue
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == p:
                    cnt += 1
    return cnt
