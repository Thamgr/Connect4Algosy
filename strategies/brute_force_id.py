import random
import time
from .base import Strategy

WIN = 100000
INF = 10 ** 9


class BruteForceID(Strategy):
    name = "brute_force_id"

    def __init__(self, max_depth=42):
        self.max_depth = max_depth

    def evaluate(self, board, time_limit):
        self.memo = {}
        moves = board.legal_moves()
        random.shuffle(moves)
        scores = {c: 0 for c in moves}
        start = time.time()
        for d in range(1, self.max_depth + 1):
            new_scores = {}
            timed_out = False
            for c in moves:
                if time.time() - start > time_limit:
                    timed_out = True
                    break
                b = board.copy()
                b.make_move(c)
                new_scores[c] = -self._negamax(b, d - 1, -INF, INF)
            if timed_out:
                break
            scores = new_scores
        return scores

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
