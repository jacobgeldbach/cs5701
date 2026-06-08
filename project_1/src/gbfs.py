import time

import pygame

from map import Cell, Terrain, get_neighbors
from stats import SearchStats
from visualization import draw_grid, draw_overlay, draw_path

# Same algorithm as UCS, except the cost to each cell is not stored in a g_cost dictionary, or even calculated
# requires a heuristic dictionary that is calculated per cell before the run of the algorithm
# For traditional heuristics I realize these should be calculated per step for that cell (|r1 - r2| + |c1 - c2| etc), and only need to be calculated for cells seen/added to the OpenList
# but I wanted to test other heuristics that could be built into a per cell dictionary via build_heuristic without completely rebuilding these algorithm methods
def gbfs(
    grid: list[list[Cell]],
    start_row: int,
    start_col: int,
    screen: pygame.Surface,
    # dictionary that maps that cells coordinates to its heuristic value for this run
    heuristic: dict[tuple[int, int], float],
) -> SearchStats:
    t_start = time.perf_counter()

    start_cell = grid[start_row][start_col]
    open_list: list[tuple[float, Cell]] = [(heuristic[(start_row, start_col)], start_cell)]
    open_set:  set[tuple[int, int]]     = {(start_row, start_col)}
    closed_set: set[tuple[int, int]]    = set()
    nodes_seen     = 1
    nodes_expanded = 0

    end_cell: Cell | None = None

    while open_list:
        h, cell = open_list.pop(0)
        open_set.discard((cell.row, cell.col))

        if cell.type == Terrain.END:
            end_cell = cell
            break

        if (cell.row, cell.col) in closed_set:
            continue

        closed_set.add((cell.row, cell.col))
        nodes_expanded += 1
        
        # When adding the neighbor Cells to the OpenList, they are coupled with their heuristic values 
        for neighbor in get_neighbors(grid, cell):
            npos = (neighbor.row, neighbor.col)
            if npos not in closed_set and npos not in open_set:
                neighbor.parent = cell
                open_list.append((heuristic[npos], neighbor))
                open_set.add(npos)
                nodes_seen += 1
        
        # That way the OpenList can then be sorted on Heuristic value only, the first entry of the tuple
        open_list.sort(key=lambda entry: entry[0])

        draw_grid(screen, grid)
        draw_overlay(screen, open_set, closed_set)
        pygame.display.flip()
        pygame.time.wait(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return SearchStats(
                    nodes_expanded, nodes_seen, len(open_set), 0, 0,
                    time.perf_counter() - t_start,
                )

    runtime = time.perf_counter() - t_start

    if end_cell is None:
        return SearchStats(nodes_expanded, nodes_seen, len(open_list), 0, 0, runtime)

    path: list[Cell] = []
    cur: Cell | None = end_cell
    while cur is not None:
        path.append(cur)
        cur = cur.parent
    path.reverse()

    draw_grid(screen, grid)
    draw_overlay(screen, open_set, closed_set)
    draw_path(screen, path)
    pygame.display.flip()

    return SearchStats(
        nodes_expanded,
        nodes_seen,
        len(open_set),
        len(path),
        sum(c.cost for c in path),
        runtime,
    )
