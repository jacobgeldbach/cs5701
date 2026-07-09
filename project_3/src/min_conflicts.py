import time
import pygame
from csp import scan_conflicts, least_conflicting_value
from stats import GenerationStats
from visualization import (
    draw_grid, draw_conflicts, draw_legend, draw_conflict_count,
)


# Repaint the whole window for the current grid: terrain, the red conflict
# overlay, the legend, and the live conflict count.
def _render(screen: pygame.Surface, grid: list[list[int]], conflicted: set) -> None:
    draw_grid(screen, grid)
    draw_conflicts(screen, conflicted)
    draw_legend(screen)
    draw_conflict_count(screen, len(conflicted))
    pygame.display.flip()


# Drain the event queue so the window stays responsive mid-search. Returns False
# if the user asked to close it.
def _pump_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


# Min-conflicts local search over the terrain CSP. Each step:
#   1. scan the grid for the most-conflicted cell (random tie-break),
#   2. reassign it the terrain value that minimizes its conflicts,
#   3. repaint so the conflict count can be watched falling.
# Runs until the grid is conflict free (solved) or max_steps is hit. Returns the
# run's GenerationStats.
def min_conflicts(grid: list[list[int]], diagonals: bool, max_steps: int,
                  screen: pygame.Surface, delay: int) -> GenerationStats:
    rows = len(grid)
    cols = len(grid[0])
    start = time.time()

    conflicted, worst = scan_conflicts(grid, diagonals)
    initial_conflicts = len(conflicted)
    _render(screen, grid, conflicted)

    steps = 0
    while worst is not None and steps < max_steps:
        if not _pump_events():
            break
        r, c = worst
        grid[r][c] = least_conflicting_value(grid, r, c, diagonals)
        steps += 1

        conflicted, worst = scan_conflicts(grid, diagonals)
        _render(screen, grid, conflicted)
        if delay:
            pygame.time.wait(delay)

    runtime = time.time() - start
    return GenerationStats(
        rows=rows,
        cols=cols,
        diagonals=diagonals,
        steps=steps,
        restarts=0,
        initial_conflicts=initial_conflicts,
        final_conflicts=len(conflicted),
        solved=(worst is None),
        runtime=runtime,
    )
