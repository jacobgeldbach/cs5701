import time

import pygame

from map import Cell, Terrain, get_neighbors
from stats import SearchStats
from visualization import draw_grid, draw_overlay, draw_path


def ucs(
    grid: list[list[Cell]],
    start_row: int,
    start_col: int,
    screen: pygame.Surface,
) -> SearchStats:
    t_start = time.perf_counter()

    start_cell = grid[start_row][start_col]
    # OpenList now has its Cells structured in tuples, where the cell is coupled with its cost to get to that cell
    open_list: list[tuple[int, Cell]]  = [(0, start_cell)]
    open_set:  set[tuple[int, int]]    = {(start_row, start_col)}
    closed_set: set[tuple[int, int]]   = set()
    # Need this dictionary to keep track of lowest cost to that cell, so duplicates of that cell can be removed from the OpenList
    g_cost: dict[tuple[int, int], int] = {(start_row, start_col): 0}
    nodes_seen     = 1
    nodes_expanded = 0

    end_cell: Cell | None = None

    # Same algorithm as BFS except after removing the Cell from the OpenList, checking if End cell, and adding it to the ClosedList
    # Neighbors are sorted by their 
    while open_list:
        cost, cell = open_list.pop(0)
        open_set.discard((cell.row, cell.col))

        if cell.type == Terrain.END:
            end_cell = cell
            break

        if (cell.row, cell.col) in closed_set:
            continue

        closed_set.add((cell.row, cell.col))
        nodes_expanded += 1

        for neighbor in get_neighbors(grid, cell):
            npos = (neighbor.row, neighbor.col)
            if npos in closed_set:
                continue
            new_cost = cost + neighbor.cost
            if npos not in open_set:
                neighbor.parent = cell
                g_cost[npos] = new_cost
                open_list.append((new_cost, neighbor))
                open_set.add(npos)
                nodes_seen += 1
            # Remove higher cost Duplicate of this Cell on the OpenList
            elif new_cost < g_cost[npos]:
                open_list = [(c, nc) for c, nc in open_list
                             if (nc.row, nc.col) != npos]
                neighbor.parent = cell
                g_cost[npos] = new_cost
                open_list.append((new_cost, neighbor))

        # Sort the OpenList by cost only, the first entry of the tuple
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
