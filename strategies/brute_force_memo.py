import math
import random
from .base import Strategy

WIN = 100000
INF = 10 ** 9
BRANCHING = 5
BASE_TIME = 3e-5  # tuned so fit_depth(1.0)=7 (~0.44s on the empirical bench)


class BruteForceMemo(Strategy):
    name = "brute_force_memo"

    def __init__(self, depth=None):
        self.depth = depth

    def evaluate(self, board, time_limit):
        depth = self.depth if self.depth is not None else self.fit_depth(time_limit)
        self.memo = {}
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
        key = (board.key(), depth)
        if key in self.memo:
            return self.memo[key]
        if board.winner() != 0:
            v = -WIN - depth
        else:
            moves = board.legal_moves()
            if not moves or depth == 0:
                v = 0
            else:
                random.shuffle(moves)
                v = -INF
                for c in moves:
                    b = board.copy()
                    b.make_move(c)
                    cv = -self._negamax(b, depth - 1)
                    if cv > v:
                        v = cv
        self.memo[key] = v
        return v
