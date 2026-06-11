import copy
from board import Board

# Do this here once instead of every step of the way for move reordering
# Essentially just starting with middle column moves since they are used in more winning windows
_MOVE_ORDER = sorted(range(7), key=lambda c: abs(c - 3))
#_MOVE_ORDER = range(7)

nodes_explored = 0
player1_nodes  = 0
player2_nodes  = 0

# Must pass in a copy of the current board as state, as min_move and max_move will alter the board state by applying moves
def mini_max(state: Board, max_depth: int, player: int, prune: bool, deepen: bool, selective: bool) -> int:
    global nodes_explored, player1_nodes, player2_nodes

    # Center-out static order (3,4,2,5,1,6,0): center moves tend to be the strongest,
    # so searching them first yields more aggressive alpha-beta cutoffs.
    order = [c for c in _MOVE_ORDER if state.is_valid_col(c)]
    best_move = order[0] if order else 0

    # Selective deepening budget: when enabled, each root-to-leaf path may spend a
    # single extension to search one ply past the depth limit on a non-quiet leaf.
    extensions = 1 if selective else 0

    # The deepen arg will allow for the _root_search() to either be iteratively be called n times from 1 to max_depth + 1
    # Else its just the stock mini_max algo call of a single run with the max_depth passed in
    depths = range(1, max_depth + 1) if deepen else (max_depth,)
    for depth in depths:
        best_move, order = _root_search(state, depth, player, prune, order, extensions)

    print(f"Player {player} nodes this turn: {nodes_explored}")
    if player == 1:
        player1_nodes += nodes_explored
    else:
        player2_nodes += nodes_explored
    nodes_explored = 0
    return best_move

# Pull out the inside of mini_max() because then if iterative_deepening is being tested, the root can be called multiple times at different depths
def _root_search(state: Board, depth: int, player: int, prune: bool, order: list[int], extensions: int) -> tuple[int, list[int]]:
    # If doing Alpha-Beta pruning, set alpha/beta; otherwise pass None to ignore them.
    alpha = float('-inf') if prune else None
    beta  = float('inf')  if prune else None
    maximum = float('-inf')
    best_move = order[0] if order else 0

    scored = []
    for move in order:
        value = min_move(state, move, 1, depth, player, extensions, alpha, beta)
        scored.append((value, move))
        if value > maximum:
            maximum = value
            best_move = move
        if prune:
            alpha = max(alpha, maximum)
        print(f"Depth {depth} | Move: {move} value: {value} | alpha={maximum:.1f} beta={beta}")

    # Best move first feeds the next deeper pass so alpha tightens immediately.
    new_order = [m for _, m in sorted(scored, key=lambda x: x[0], reverse=True)]
    return best_move, new_order

def min_move(state: Board, move: int, current_depth: int, max_depth: int, player: int, extensions: int = 0, alpha: float=None, beta: float=None) -> float:
    global nodes_explored
    nodes_explored += 1
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

    if (current_depth >= max_depth):
        result, threat = state.eval(player)
        # Selective deepening: a non-quiet leaf (a win/loss available next turn)
        # spends the path's single extension and is searched one ply deeper so the
        # threat is resolved instead of trusting the static estimate. Otherwise the
        # estimate is returned as the leaf value.
        if extensions > 0 and threat:
            max_depth += 1
            extensions -= 1
        else:
            state.undo_piece(move)
            return result

    minimum = float('inf')
    # For move reordering sort the columns list from the center (3,2,4,1,5,0,6) it makes sense to search the center column moves first, as those will tend to be the higher scoring/better moves
    # This will in turn lead to more aggressive pruning when alpha beta pruning is turned on
    for m in _MOVE_ORDER:
        if not state.is_valid_col(m):
            continue
        value = max_move(state, m, current_depth + 1, max_depth, player, extensions, alpha, beta)
        if (value < minimum):
            minimum = value
        
        # Alpha-beta pruning
        if (alpha is not None and beta is not None):
            if value < beta:
                beta = min(beta, value)
            if (beta <= alpha):
                break

    state.undo_piece(move)

    return minimum

def max_move(state: Board, move: int, current_depth: int, max_depth: int, player: int, extensions: int = 0, alpha: float=None, beta: float=None) -> float:
    global nodes_explored
    nodes_explored += 1
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

    if (current_depth >= max_depth):
        result, threat = state.eval(player)
        # Selective deepening: a non-quiet leaf (a win/loss available next turn)
        # spends the path's single extension and is searched one ply deeper so the
        # threat is resolved instead of trusting the static estimate. Otherwise the
        # estimate is returned as the leaf value.
        if extensions > 0 and threat:
            max_depth += 1
            extensions -= 1
        else:
            state.undo_piece(move)
            return result

    maximum = float('-inf')
    for m in _MOVE_ORDER:
        if not state.is_valid_col(m):
            continue
        value = min_move(state, m, current_depth + 1, max_depth, player, extensions, alpha, beta)
        if (value > maximum):
            maximum = value
        
        # Alpha-beta pruning
        if (alpha is not None and beta is not None):
            if value > alpha:
                alpha = max(alpha, value)
            if (alpha >= beta):
                # Immediately break and return maximum as there is no need to check the rest of this branch since the opponent will never let us get here
                break

    state.undo_piece(move)
    
    return maximum
