from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Terrain(Enum):
    ROAD      = 'R'
    FIELD     = 'F'
    FOREST    = 'O'
    HILLS     = 'H'
    MOUNTAINS = 'M'
    WATER     = 'W'
    START     = 'S'
    END       = 'E'


_COST = {
    Terrain.ROAD:      1,
    Terrain.FIELD:     3,
    Terrain.FOREST:    5,
    Terrain.HILLS:     8,
    Terrain.MOUNTAINS: 15,
    Terrain.WATER:     0,
    Terrain.START:     0,
    Terrain.END:       0,
}


@dataclass
class Cell:
    type:   Terrain
    cost:   int
    row:    int
    col:    int
    parent: Cell | None = field(default=None, repr=False)

    @classmethod
    def from_char(cls, char: str, row: int, col: int) -> Cell:
        terrain = Terrain(char)
        return cls(type=terrain, cost=_COST[terrain], row=row, col=col)

# Read the map input file, process each character into a cell struct and save it in the grid double list
# Returns the double list of Cells defining the map, coordinates of the start cell and coordinates of the end cell
def map_read_process(map_path: str) -> tuple[list[list[Cell]], int, int, int, int]:
    grid: list[list[Cell]] = []
    start_row, start_col = -1, -1
    end_row,   end_col   = -1, -1

    with open(map_path, 'r') as f:
        for row_idx, line in enumerate(f):
            row: list[Cell] = []
            for col_idx, char in enumerate(line.rstrip('\n')):
                cell = Cell.from_char(char, row_idx, col_idx)
                # Save the Start cell
                if cell.type == Terrain.START:
                    start_row, start_col = row_idx, col_idx
                elif cell.type == Terrain.END:
                    end_row, end_col = row_idx, col_idx
                row.append(cell)
            grid.append(row)

    return grid, start_row, start_col, end_row, end_col

# Returns 
def get_neighbors(grid: list[list[Cell]], cell: Cell) -> list[Cell]:
    rows = len(grid)
    cols = len(grid[0])
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = cell.row + dr, cell.col + dc
        if 0 <= r < rows and 0 <= c < cols:
            neighbor = grid[r][c]
            if neighbor.type != Terrain.WATER:
                neighbors.append(neighbor)
    return neighbors
