from enviroment import Board


def play_game(strat_x, strat_o, time_limit=1.0):
    board = Board()
    history = [board.copy()]
    while not board.is_terminal():
        strat = strat_x if board.player == 1 else strat_o
        col = strat.choose(board.copy(), time_limit)
        board.make_move(col)
        history.append(board.copy())
    return board.winner(), history
