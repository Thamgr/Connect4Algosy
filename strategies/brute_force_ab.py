import math
import random
from .base import Strategy

WIN = 100000
INF = 10 ** 9
BRANCHING = 3
BASE_TIME = 1e-4  # tuned so fit_depth(1.0)=9 (αβ keeps depth-7 around 0.03s on the bench)


class BruteForceAB(Strategy):
    name = "brute_force_ab"

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
            scores[c] = -self._negamax(b, depth - 1, -INF, INF)
        return scores

    def fit_depth(self, time_limit):
        if time_limit <= BASE_TIME:
            return 1
        return 1 + int(math.log(time_limit / BASE_TIME, BRANCHING))

    def _negamax(self, board, depth, alpha, beta):
        key = (board.key(), depth)
        if key in self.memo:
            v, flag = self.memo[key]
            if flag == 'exact':
                return v
            if flag == 'lower' and v >= beta:
                return v
            if flag == 'upper' and v <= alpha:
                return v
        a0 = alpha
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
            v = -self._negamax(b, depth - 1, -beta, -alpha)
            if v > best:
                best = v
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        flag = 'upper' if best <= a0 else 'lower' if best >= beta else 'exact'
        self.memo[key] = (best, flag)
        return best
