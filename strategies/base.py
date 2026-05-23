class Strategy:
    name = "strategy"

    def choose(self, board, time_limit):
        scores = self.evaluate(board, time_limit)
        return max(scores, key=scores.get)

    def evaluate(self, board, time_limit):
        raise NotImplementedError
