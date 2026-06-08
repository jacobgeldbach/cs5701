from collections import deque
import time

import pygame

from map import Cell, Terrain, get_neighbors
from stats import SearchStats
from visualization import draw_grid, draw_overlay, draw_path


def bfs(
    grid: list[list[Cell]],
    start_row: int,
    start_col: int,
    screen: pygame.Surface,
) -> SearchStats:
    t_start = time.perf_counter()


    # Get the start cell and add it to the open_list
    start_cell = grid[start_row][start_col]
    open_list: deque[Cell] = deque([start_cell])
    open_set: set[tuple[int, int]]    = {(start_row, start_col)}
    closed_set: set[tuple[int, int]]  = set()
    nodes_seen     = 1
    nodes_expanded = 0

    end_cell: Cell | None = None
    
    # Repeat until End cell is found or all Cells have been seen and explored (added and removed from OpenList)
    while open_list:
        cell = open_list.popleft()
        open_set.discard((cell.row, cell.col))

        # BFS ends when the goal state is REMOVED from the OpenList, not added (seen)
        if cell.type == Terrain.END:
            end_cell = cell
            break

        # Cell already explored
        if (cell.row, cell.col) in closed_set:
            continue

        # Set is used instead of list for faster searching (the above check and the check below) as opposed to a python list, believe its O(1) instead of O(n)
        closed_set.add((cell.row, cell.col))
        nodes_expanded += 1

        # Add all of its neighbors not in ClosedList
        for neighbor in get_neighbors(grid, cell):
            if (neighbor.row, neighbor.col) not in closed_set:
                if neighbor.parent is None:
                    neighbor.parent = cell
                open_list.append(neighbor)
                open_set.add((neighbor.row, neighbor.col))
                nodes_seen += 1

        # The way pygame works is you write to a buffer (screen) thats "behind" the one currently being displayed in the visualization
        # then once .flip() is called it swaps the screen with the new display data that was just written
        draw_grid(screen, grid)
        draw_overlay(screen, open_set, closed_set)
        pygame.display.flip()
        pygame.time.wait(10) # Added for visualization purposes, so both closed and open list cells can be seen growing

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
