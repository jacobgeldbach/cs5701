import random
import terrain

# Neighbor offsets. The four orthogonal neighbors (up/down/left/right) are always
# used; the four diagonals are added only in the 8-neighbor experimental
# condition. The grid does not wrap, so out-of-bounds offsets are skipped.
_ORTHO = [(-1, 0), (1, 0), (0, -1), (0, 1)]
_DIAG  = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def _offsets(diagonals: bool) -> list[tuple[int, int]]:
    return _ORTHO + _DIAG if diagonals else _ORTHO


# Collect the values of a cell's in-bounds neighbors (2-8 of them depending on
# position and the diagonal setting). Gathering them once lets a candidate value
# be scored without re-walking the grid.
def _neighbor_values(grid: list[list[int]], r: int, c: int, diagonals: bool) -> list[int]:
    rows = len(grid)
    cols = len(grid[0])
    values = []
    for dr, dc in _offsets(diagonals):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            values.append(grid[nr][nc])
    return values


# Conflicts a value would have against a fixed set of neighbor values: a neighbor
# conflicts when it differs by more than one elevation step (|a - b| > 1).
def _conflicts_against(value: int, neighbor_values: list[int]) -> int:
    return sum(1 for nv in neighbor_values if abs(value - nv) > 1)


# Count how many of a cell's in-bounds neighbors currently violate the adjacency
# rule.
def cell_conflicts(grid: list[list[int]], r: int, c: int, diagonals: bool) -> int:
    return _conflicts_against(grid[r][c], _neighbor_values(grid, r, c, diagonals))


# One full pass over the grid. Returns (conflicted, worst, total):
#   conflicted -- the set of every (row, col) with at least one conflict, used
#                 for the red overlay and the live "Conflicts: N" readout.
#   worst      -- a cell chosen at random from those tied for the most conflicts
#                 (ties are common, so the random pick keeps the search from
#                 always working the same corner), or None when the grid is
#                 conflict free, which is the solved state. Used by the default
#                 most-conflicted-first mode; --classic ignores it.
#   total      -- the sum of every cell's conflict count (each violating edge
#                 counted twice). This is the progress metric the stopping
#                 criterion watches: unlike the conflicted-cell count it drops
#                 when a cell goes from, say, 4 conflicts to 1, so genuine
#                 progress that doesn't fully clear a cell still registers.
def scan_conflicts(grid: list[list[int]],
                   diagonals: bool) -> tuple[set[tuple[int, int]], tuple[int, int] | None, int]:
    conflicted = set()
    total = 0
    best_count = 0
    best_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            n = cell_conflicts(grid, r, c, diagonals)
            if n == 0:
                continue
            conflicted.add((r, c))
            total += n
            if n > best_count:
                best_count = n
                best_cells = [(r, c)]
            elif n == best_count:
                best_cells.append((r, c))
    worst = random.choice(best_cells) if best_cells else None
    return conflicted, worst, total


# Min-conflicts value selection: of the six terrains, pick the one that leaves
# the chosen cell with the fewest conflicting neighbors. Ties (including the
# cell's current value) are broken at random so the search can move sideways
# across plateaus instead of locking in place.
def least_conflicting_value(grid: list[list[int]], r: int, c: int, diagonals: bool) -> int:
    neighbor_values = _neighbor_values(grid, r, c, diagonals)
    best_count = None
    best_values = []
    for value in range(terrain.NUM_TERRAINS):
        n = _conflicts_against(value, neighbor_values)
        if best_count is None or n < best_count:
            best_count = n
            best_values = [value]
        elif n == best_count:
            best_values.append(value)
    return random.choice(best_values)
