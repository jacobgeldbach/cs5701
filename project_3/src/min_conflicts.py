import random
import time
import pygame
from csp import scan_conflicts, least_conflicting_value
from stats import GenerationStats
from visualization import (
    draw_grid, draw_conflicts, draw_legend, draw_conflict_count,
)

# In windowed mode the grid is repainted every this many steps rather than every
# step: on large grids a full repaint (one rect per cell) costs as much as the
# search itself, so drawing every step dominates runtime. 50 keeps the animation
# smooth while cutting draw cost ~50x. --headless skips drawing entirely.
_RENDER_EVERY = 50


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
#   1. choose a conflicted cell --
#        default : one of the cells tied for the MOST conflicts (random pick),
#        classic : any conflicted cell, uniformly at random (textbook variant),
#   2. reassign it the terrain value that minimizes its conflicts,
#   3. repaint so the conflict count can be watched falling.
#
# Stopping: the search ends when the grid is conflict free (solved), or when it
# goes `patience` steps without lowering the best total-conflict count seen
# (steps_since_improvement) -- a stagnation signal that catches local minima and
# plateaus. max_steps is only a hard safety cap (0 = no cap); patience is the
# primary criterion.
#
# The search wanders, so the grid at the moment it stops is usually not the best
# grid it passed through. We snapshot the lowest-conflict grid seen and restore
# it before returning, so the map we hand back (and visualize) is the best one.
#
# screen is None in --headless mode: the search then does no drawing, event
# pumping, or delay at all, which is the fast path for large grids and batch runs.
def min_conflicts(grid: list[list[int]], diagonals: bool, patience: int,
                  max_steps: int, classic: bool,
                  screen: pygame.Surface | None, delay: int) -> GenerationStats:
    rows = len(grid)
    cols = len(grid[0])
    headless = screen is None
    start = time.time()

    conflicted, worst, total = scan_conflicts(grid, diagonals)
    initial_conflicts = len(conflicted)
    if not headless:
        _render(screen, grid, conflicted)

    best_total = total
    best_grid = [row[:] for row in grid]
    steps_since_improvement = 0

    steps = 0
    while (conflicted
           and steps_since_improvement < patience
           and (max_steps == 0 or steps < max_steps)):
        if not headless and not _pump_events():
            break
        if classic:
            r, c = random.choice(list(conflicted))
        else:
            r, c = worst
        grid[r][c] = least_conflicting_value(grid, r, c, diagonals)
        steps += 1

        conflicted, worst, total = scan_conflicts(grid, diagonals)
        if total < best_total:
            best_total = total
            best_grid = [row[:] for row in grid]
            steps_since_improvement = 0
        else:
            steps_since_improvement += 1

        if not headless and steps % _RENDER_EVERY == 0:
            _render(screen, grid, conflicted)
            if delay:
                pygame.time.wait(delay)

    # Restore the best grid seen and repaint so the final view matches the map
    # we report and return.
    for r in range(rows):
        grid[r] = best_grid[r]
    final_conflicted, _, best_total = scan_conflicts(grid, diagonals)
    if not headless:
        _render(screen, grid, final_conflicted)

    runtime = time.time() - start
    return GenerationStats(
        rows=rows,
        cols=cols,
        diagonals=diagonals,
        classic=classic,
        steps=steps,
        restarts=0,
        initial_conflicts=initial_conflicts,
        final_conflicts=len(final_conflicted),
        solved=(best_total == 0),
        runtime=runtime,
    )
