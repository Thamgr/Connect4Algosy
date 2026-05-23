ROWS, COLS = 6, 7


class Board:
    def __init__(self):
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.heights = [0] * COLS
        self.player = 1
        self.last = None

    def legal_moves(self):
        return [c for c in range(COLS) if self.heights[c] < ROWS]

    def make_move(self, col):
        row = self.heights[col]
        self.grid[row][col] = self.player
        self.heights[col] += 1
        self.last = (row, col, self.player)
        self.player = -self.player

    def winner(self):
        if self.last is None:
            return 0
        r, c, p = self.last
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count = 1
            for sign in (1, -1):
                rr, cc = r + sign * dr, c + sign * dc
                while 0 <= rr < ROWS and 0 <= cc < COLS and self.grid[rr][cc] == p:
                    count += 1
                    rr += sign * dr
                    cc += sign * dc
            if count >= 4:
                return p
        return 0

    def is_terminal(self):
        return self.winner() != 0 or all(h == ROWS for h in self.heights)

    def copy(self):
        b = Board.__new__(Board)
        b.grid = [row[:] for row in self.grid]
        b.heights = self.heights[:]
        b.player = self.player
        b.last = self.last
        return b

    def key(self):
        return (tuple(tuple(row) for row in self.grid), self.player)

    def __str__(self):
        sym = {0: '.', 1: 'X', -1: 'O'}
        lines = []
        for r in reversed(range(ROWS)):
            lines.append(' '.join(sym[self.grid[r][c]] for c in range(COLS)))
        lines.append(' '.join(str(i) for i in range(COLS)))
        return '\n'.join(lines)
