import copy
from board import Board
from board import MAX_DEPTH

# Must pass in a copy of the current board as state, as minMove and maxMove will alter the board state by applying moves
def mini_max(state: Board, depth: int, player: int) -> int:
    best_move = 0
    maximum = float('-inf')

    for move in state.get_valid_cols():
        value = max_move(copy.deepcopy(state), move, depth, player)
        print(f"Potential move: {move} value: {value}")
        if (value > maximum):
            maximum = value
            best_move = move

    return best_move

def min_move(state: Board, move: int, depth: int, player: int) -> float:
    opponent = 1 if player == 2 else 2
    state.drop_piece(move, opponent)

    # Check if AI won
    if (state.check_win(player)):
        return float('inf')

    # this is checking if opponent won aka AI lose
    if (state.check_win(opponent)):
        return float('-inf')

    if (state.is_draw()):
        return 0

    if (depth == MAX_DEPTH):
        return state.eval(player)

    minimum = float('inf')
    for m in state.get_valid_cols():
        value = max_move(copy.deepcopy(state), m, depth + 1, player)
        if (value < minimum):
            minimum = value

    return minimum

def max_move(state: Board, move: int, depth: int, player: int) -> float:
    opponent = 1 if player == 2 else 2
    state.drop_piece(move, player)

    # Check if AI won
    if (state.check_win(player)):
        return float('inf')

    # this is checking if opponent won aka AI lose
    if (state.check_win(opponent)):
        return float('-inf')

    if (state.is_draw()):
        return 0

    if (depth == MAX_DEPTH):
        return state.eval(player)

    maximum = float('-inf')
    for m in state.get_valid_cols():
        value = min_move(copy.deepcopy(state), m, depth + 1, player)
        if (value > maximum):
            maximum = value

    return maximum
