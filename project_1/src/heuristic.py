from map import Cell, Terrain, get_neighbors

MANHATTAN             = 'manhattan'
REVERSED_UCS          = 'reversed_ucs'
AVG_WEIGHTED_MANHATTAN = 'avg_weighted_manhattan'


def build_heuristic(
    grid: list[list[Cell]],
    end_row: int,
    end_col: int,
    method: str = MANHATTAN,
) -> dict[tuple[int, int], float]:
    if method == REVERSED_UCS:
        return _build_reversed_ucs(grid, end_row, end_col)
    if method == AVG_WEIGHTED_MANHATTAN:
        return _build_avg_weighted_manhattan(grid, end_row, end_col)
    return _build_manhattan(grid, end_row, end_col)

# Admissable heuristic, although grossly underestimates 
def _build_manhattan(
    grid: list[list[Cell]],
    end_row: int,
    end_col: int,
) -> dict[tuple[int, int], float]:
    h = {}
    for row in grid:
        for cell in row:
            pos = (cell.row, cell.col)
            if cell.type == Terrain.WATER:
                h[pos] = float('inf')
            else:
                h[pos] = abs(cell.row - end_row) + abs(cell.col - end_col)
    return h

# Non-admissable heuristic as the average cost weight for some manhattan paths (weight * |a1 - a2| + |b1 - b2|) will overestimate some of the paths
def _build_avg_weighted_manhattan(
    grid: list[list[Cell]],
    end_row: int,
    end_col: int,
) -> dict[tuple[int, int], float]:
    traversable = [cell for row in grid for cell in row
                   if cell.type != Terrain.WATER]
    avg_cost = sum(cell.cost for cell in traversable) / len(traversable)

    h = {}
    for row in grid:
        for cell in row:
            pos = (cell.row, cell.col)
            if cell.type == Terrain.WATER:
                h[pos] = float('inf')
            else:
                h[pos] = avg_cost * (abs(cell.row - end_row) + abs(cell.col - end_col))
    return h

# This produces a perfect heuristic value (also takes out the point of running the algorithm) but I did this for my own tests/intrigue
def _build_reversed_ucs(
    grid: list[list[Cell]],
    end_row: int,
    end_col: int,
) -> dict[tuple[int, int], float]:
    end_cell = grid[end_row][end_col]
    open_list: list[tuple[float, Cell]]  = [(0, end_cell)]
    open_set:  set[tuple[int, int]]      = {(end_row, end_col)}
    closed_set: set[tuple[int, int]]     = set()
    g_cost: dict[tuple[int, int], float] = {(end_row, end_col): 0}

    while open_list:
        cost, cell = open_list.pop(0)
        open_set.discard((cell.row, cell.col))

        if (cell.row, cell.col) in closed_set:
            continue

        closed_set.add((cell.row, cell.col))

        for neighbor in get_neighbors(grid, cell):
            npos = (neighbor.row, neighbor.col)
            if npos in closed_set:
                continue
            new_cost = cost + cell.cost
            if npos not in open_set:
                g_cost[npos] = new_cost
                open_list.append((new_cost, neighbor))
                open_set.add(npos)
            elif new_cost < g_cost[npos]:
                open_list = [(c, nc) for c, nc in open_list
                             if (nc.row, nc.col) != npos]
                g_cost[npos] = new_cost
                open_list.append((new_cost, neighbor))

        open_list.sort(key=lambda entry: entry[0])

    h = {}
    for row in grid:
        for cell in row:
            pos = (cell.row, cell.col)
            if cell.type == Terrain.WATER:
                h[pos] = float('inf')
            else:
                h[pos] = g_cost.get(pos, float('inf'))
    return h
