import random
from .base import Strategy


class RandomStrategy(Strategy):
    name = "random"

    def evaluate(self, board, time_limit):
        return {c: random.random() for c in board.legal_moves()}
