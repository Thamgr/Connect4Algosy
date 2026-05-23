import math
import random
import time
from .base import Strategy


class Node:
    __slots__ = ('parent', 'move', 'player', 'children', 'visits', 'wins', 'untried')

    def __init__(self, board, parent=None, move=None):
        self.parent = parent
        self.move = move
        self.player = board.player
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried = board.legal_moves() if not board.is_terminal() else []


class MCTS(Strategy):
    name = "mcts"
    C = 1.41

    def evaluate(self, board, time_limit):
        root = Node(board)
        start = time.time()
        while time.time() - start < time_limit:
            sim_board = board.copy()
            leaf = self.selection(root, sim_board)
            leaf = self.expansion(leaf, sim_board)
            winner = self.simulation(sim_board)
            self.backpropagation(leaf, winner)
        return {ch.move: ch.visits for ch in root.children}

    def selection(self, node, board):
        while not node.untried and node.children:
            log_n = math.log(node.visits)
            node = max(node.children, key=lambda ch: ch.wins / ch.visits + self.C * math.sqrt(log_n / ch.visits))
            board.make_move(node.move)
        return node

    def expansion(self, node, board):
        if not node.untried:
            return node
        move = node.untried.pop(random.randrange(len(node.untried)))
        board.make_move(move)
        child = Node(board, parent=node, move=move)
        node.children.append(child)
        return child

    def simulation(self, board):
        while not board.is_terminal():
            board.make_move(random.choice(board.legal_moves()))
        return board.winner()

    def backpropagation(self, node, winner):
        while node is not None:
            node.visits += 1
            mover = -node.player
            if winner == mover:
                node.wins += 1
            elif winner == 0:
                node.wins += 0.5
            node = node.parent
