import copy
from board import Board

# Do this here once instead of every step of the way for move reordering
_MOVE_ORDER = sorted(range(7), key=lambda c: abs(c - 3))

# Must pass in a copy of the current board as state, as minMove and maxMove will alter the board state by applying moves
def mini_max(state: Board, max_depth: int, player: int, prune: bool) -> int:
    best_move = 0
    maximum = float('-inf')

    # For move reordering sort the columns list from the center (3,4,2,5,1,6,0) it makes sense to search the center column moves first, as those will tend to be the higher scoring/better moves
    # This will in turn lead to more aggressive pruning when alpha beta pruning is turned on
    for move in state.get_valid_cols():
        if not state.is_valid_col(move):
            continue
        # If doing Alpha Beta pruning, pass in alpha and beta range values, otherwise pass in None to ignore them
        value = max_move(state, move, 0, max_depth, player, float('-inf') if prune else None, float('inf') if prune else None)
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
        state.undo_piece(move)
        return float('inf')

    # this is checking if opponent won aka AI lose
    if (state.check_win(opponent)):
        state.undo_piece(move)
        return float('-inf')

    if (state.is_draw()):
        state.undo_piece(move)
        return 0

    if (current_depth == max_depth):
        result = state.eval(player)
        state.undo_piece(move)
        return result

    minimum = float('inf')
    # For move reordering sort the columns list from the center (3,2,4,1,5,0,6) it makes sense to search the center column moves first, as those will tend to be the higher scoring/better moves
    # This will in turn lead to more aggressive pruning when alpha beta pruning is turned on
    for m in state.get_valid_cols():
        if not state.is_valid_col(m):
            continue
        value = max_move(state, m, current_depth + 1, max_depth, player, alpha, beta)
        if (value < minimum):
            minimum = value
        
        # Alpha-beta pruning
        if (alpha is not None and beta is not None):
            beta = min(beta, value)
            if (alpha >= beta):
                # Immediately break and return maximum as there is no need to check the rest of this branch since the opponent will never let us get here
                break

    state.undo_piece(move)

    return minimum

def max_move(state: Board, move: int, current_depth: int, max_depth: int, player: int, alpha: float=None, beta: float=None) -> float:
    opponent = 1 if player == 2 else 2
    state.drop_piece(move, player)

    # Check if AI won
    if (state.check_win(player)):
        state.undo_piece(move)
        return float('inf')

    # this is checking if opponent won aka AI lose
    if (state.check_win(opponent)):
        state.undo_piece(move)
        return float('-inf')

    if (state.is_draw()):
        state.undo_piece(move)
        return 0

    if (current_depth == max_depth):
        result = state.eval(player)
        state.undo_piece(move)
        return result

    maximum = float('-inf')
    # For move reordering sort the columns list from the center (3,4,2,5,1,6,0) it makes sense to search the center column moves first, as those will tend to be the higher scoring/better moves
    # This will in turn lead to more aggressive pruning when alpha beta pruning is turned on
    for m in state.get_valid_cols():
        #for m in _MOVE_ORDER:
        if not state.is_valid_col(m):
            continue
        value = min_move(state, m, current_depth + 1, max_depth, player, alpha, beta)
        if (value > maximum):
            maximum = value
        
        # Alpha-beta pruning
        if (alpha is not None and beta is not None):
            alpha = max(alpha, value)
            if (beta <= alpha):
                # Immediately break and return maximum as there is no need to check the rest of this branch since the opponent will never let us get here
                break

    state.undo_piece(move)
    
    return maximum
