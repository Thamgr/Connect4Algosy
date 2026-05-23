import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies import (
    RandomStrategy,
    BruteForce,
    BruteForceEval,
    BruteForceMemo,
    BruteForceAB,
    BruteForceID,
    MCTS,
)

STRATS = {
    'random': lambda: RandomStrategy(),
    'bf': lambda: BruteForce(),
    'bf_eval': lambda: BruteForceEval(),
    'bf_memo': lambda: BruteForceMemo(),
    'bf_ab': lambda: BruteForceAB(),
    'bf_id': lambda: BruteForceID(),
    'mcts': lambda: MCTS(),
}
