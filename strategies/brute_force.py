import math
import random
from .base import Strategy

WIN = 100000
INF = 10 ** 9
BRANCHING = 7
BASE_TIME = 3e-5  # tuned so fit_depth(1.0)=6 (~0.37s on the empirical bench)


class BruteForce(Strategy):
    name = "brute_force"

    def __init__(self, depth=None):
        self.depth = depth

    def evaluate(self, board, time_limit):
        depth = self.depth if self.depth is not None else self.fit_depth(time_limit)
        scores = {}
        moves = board.legal_moves()
        random.shuffle(moves)
        for c in moves:
            b = board.copy()
            b.make_move(c)
            scores[c] = -self._negamax(b, depth - 1)
        return scores

    def fit_depth(self, time_limit):
        if time_limit <= BASE_TIME:
            return 1
        return 1 + int(math.log(time_limit / BASE_TIME, BRANCHING))

    def _negamax(self, board, depth):
        if board.winner() != 0:
            return -WIN - depth
        moves = board.legal_moves()
        if not moves or depth == 0:
            return 0
        random.shuffle(moves)
        best = -INF
        for c in moves:
            b = board.copy()
            b.make_move(c)
            v = -self._negamax(b, depth - 1)
            if v > best:
                best = v
        return best
