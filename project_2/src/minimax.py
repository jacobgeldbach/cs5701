import copy
from board import Board

# Must pass in a copy of the current board as state, as minMove and maxMove will alter the board state by applying moves
def mini_max(state: Board, max_depth: int, player: int, prune: bool) -> int:
    best_move = 0
    maximum = float('-inf')

    for move in state.get_valid_cols():
        # If doing Alpha Beta pruning, pass in alpha and beta range values, otherwise pass in None to ignore them
        value = max_move(copy.deepcopy(state), move, 0, max_depth, player, float('-inf') if prune else None, float('inf') if prune else None)
        print(f"Potential move: {move} value: {value}")
        if (value > maximum):
            maximum = value
            best_move = move
        
    return best_move

def min_move(state: Board, move: int, current_depth: int, max_depth: int, player: int, alpha: float=None, beta: float=None) -> float:
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

    if (current_depth == max_depth):
        return state.eval(player)

    minimum = float('inf')
    for m in state.get_valid_cols():
        value = max_move(copy.deepcopy(state), m, current_depth + 1, max_depth, player, alpha, beta)
        if (value < minimum):
            minimum = value
        
        # Alpha-beta pruning
        if (alpha is not None and beta is not None):
            beta = min(beta, value)
            if (alpha >= beta):
                # Immediately break and return maximum as there is no need to check the rest of this branch since the opponent will never let us get here
                break 

    return minimum

def max_move(state: Board, move: int, current_depth: int, max_depth: int, player: int, alpha: float=None, beta: float=None) -> float:
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

    if (current_depth == max_depth):
        return state.eval(player)

    maximum = float('-inf')
    for m in state.get_valid_cols():
        value = min_move(copy.deepcopy(state), m, current_depth + 1, max_depth, player, alpha, beta)
        if (value > maximum):
            maximum = value
        
        # Alpha-beta pruning
        if (alpha is not None and beta is not None):
            alpha = max(alpha, value)
            if (beta <= alpha):
                # Immediately break and return maximum as there is no need to check the rest of this branch since the opponent will never let us get here
                break

    return maximum
