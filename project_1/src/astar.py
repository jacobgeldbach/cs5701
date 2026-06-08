import time

import pygame

from map import Cell, Terrain, get_neighbors
from stats import SearchStats
from visualization import draw_grid, draw_overlay, draw_path


def astar(
    grid: list[list[Cell]],
    start_row: int,
    start_col: int,
    screen: pygame.Surface,
    heuristic: dict[tuple[int, int], float],
) -> SearchStats:
    t_start = time.perf_counter()

    start_cell = grid[start_row][start_col]
    start_pos  = (start_row, start_col)
    open_list: list[tuple[float, Cell]]  = [(heuristic[start_pos], start_cell)]
    open_set:  set[tuple[int, int]]      = {start_pos}
    closed_set: set[tuple[int, int]]     = set()
    g_cost: dict[tuple[int, int], float] = {start_pos: 0}
    nodes_seen     = 1
    nodes_expanded = 0

    # A* being the most involved, as it requires the dictionary that describes the cost to that cell (g_cost) and the heuristic dictionary mapping the cell to 
    # its heuristic values for this run 
    end_cell: Cell | None = None

    while open_list:
        _, cell = open_list.pop(0)
        open_set.discard((cell.row, cell.col))

        if cell.type == Terrain.END:
            end_cell = cell
            break

        if (cell.row, cell.col) in closed_set:
            continue

        closed_set.add((cell.row, cell.col))
        nodes_expanded += 1

        cell_g = g_cost[(cell.row, cell.col)]

        # Same as UCS where the OpenList duplicates are removed, only keeping the copy of that Cell on the OpenList with the smaller. Had to think about this
        # but the reason for it is that if a Cell is in the found path we would never take the longer way to get there 
        for neighbor in get_neighbors(grid, cell):
            npos = (neighbor.row, neighbor.col)
            if npos in closed_set:
                continue
            new_g = cell_g + neighbor.cost
            if npos not in open_set:
                neighbor.parent = cell
                g_cost[npos] = new_g
                open_list.append((new_g + heuristic[npos], neighbor))
                open_set.add(npos)
                nodes_seen += 1
            elif new_g < g_cost[npos]:
                open_list = [(f, nc) for f, nc in open_list
                             if (nc.row, nc.col) != npos]
                neighbor.parent = cell
                g_cost[npos] = new_g
                open_list.append((new_g + heuristic[npos], neighbor))

        # In the above step, UCS and GBFS methods are essentially combined, coupling the Cells on the OpenList with their Heuristic value + cost to travel to that cell
        # Sort OpenList on this value
        open_list.sort(key=lambda entry: entry[0])

        draw_grid(screen, grid)
        draw_overlay(screen, open_set, closed_set)
        pygame.display.flip()
        pygame.time.wait(10)

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
