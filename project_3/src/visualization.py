import os
import pygame
import terrain

# Give pygame a dummy audio driver so it does not try (and fail) to open a real
# one under WSL2 -- same fix used in project_1 and project_2.
os.environ['SDL_AUDIODRIVER'] = 'dummy'

_BASE_COLOR = {
    terrain.WATER:     ( 30, 100, 200),
    terrain.BEACH:     (237, 201, 145),
    terrain.LOWLAND:   (170, 210, 130),
    terrain.FOREST:    ( 34, 110,  45),
    terrain.HILLS:     (150, 120,  75),
    terrain.MOUNTAINS: (120, 110, 110),
}

_SEPARATOR     = (40, 40, 40)
_PANEL_BG      = (20, 20, 20, 210)
_CONFLICT_FILL = (220, 30, 30, 150)

# Grids range from 50x50 up to 200x200, so the cell size is computed from the
# grid dimensions to keep the window within a sensible pixel budget rather than
# being fixed. _MAX_SLOT caps the cell size so small grids do not balloon.
_MAX_GRID_PX = 900
_MAX_SLOT    = 18

# Layout, filled in by _configure_layout() from the grid in init_display.
CELL_SIZE = 0
_GAP      = 0
_SLOT     = 0

_LEGEND_PAD    = 9
_LEGEND_ITEM_H = 26
_LEGEND_SWATCH = 18


def _configure_layout(grid: list) -> None:
    global CELL_SIZE, _GAP, _SLOT
    rows = len(grid)
    cols = len(grid[0])
    _SLOT = min(_MAX_SLOT, max(2, _MAX_GRID_PX // max(rows, cols)))
    _GAP  = 1 if _SLOT >= 6 else 0
    CELL_SIZE = _SLOT - _GAP


def _win_size(grid: list) -> tuple[int, int]:
    rows = len(grid)
    cols = len(grid[0])
    return cols * _SLOT + _GAP, rows * _SLOT + _GAP


# Initialize the pygame "screen" and draw the initial state of the generated map.
def init_display(grid: list) -> pygame.Surface:
    pygame.init()
    _configure_layout(grid)
    screen = pygame.display.set_mode(_win_size(grid))
    pygame.display.set_caption('Terrain Map Generation')
    draw_grid(screen, grid)
    draw_legend(screen)
    pygame.display.flip()
    return screen


# Draw every cell of the grid color-coded by its terrain integer.
def draw_grid(screen: pygame.Surface, grid: list) -> None:
    screen.fill(_SEPARATOR)
    for row, row_vals in enumerate(grid):
        for col, value in enumerate(row_vals):
            x = col * _SLOT + _GAP
            y = row * _SLOT + _GAP
            pygame.draw.rect(screen, _BASE_COLOR[value], (x, y, CELL_SIZE, CELL_SIZE))


# Tint every conflicted cell red, keeping its terrain color visible underneath.
# Called per min-conflicts step so the search can be watched repairing the map.
# conflicts is an iterable of (row, col) tuples.
def draw_conflicts(screen: pygame.Surface, conflicts) -> None:
    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    overlay.fill(_CONFLICT_FILL)
    for row, col in conflicts:
        x = col * _SLOT + _GAP
        y = row * _SLOT + _GAP
        screen.blit(overlay, (x, y))


# Live readout of how many cells currently violate an adjacency constraint,
# drawn in the bottom-right corner. Called once per min-conflicts step so the
# count can be watched dropping toward zero as the search repairs the map.
def draw_conflict_count(screen: pygame.Surface, count: int) -> None:
    font = pygame.font.SysFont('monospace', 16, bold=True)
    text = font.render(f"Conflicts: {count}", True, (230, 230, 230))

    pad = 8
    box_w = text.get_width() + pad * 2
    box_h = text.get_height() + pad * 2
    x0 = screen.get_width() - box_w - 5
    y0 = screen.get_height() - box_h - 5

    bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    bg.fill(_PANEL_BG)
    screen.blit(bg, (x0, y0))
    screen.blit(text, (x0 + pad, y0 + pad))


def draw_legend(screen: pygame.Surface) -> None:
    font = pygame.font.SysFont('monospace', 14)
    items = [(_BASE_COLOR[t], terrain.NAME[t]) for t in range(terrain.NUM_TERRAINS)]
    items.append((_CONFLICT_FILL[:3], 'Conflict'))

    legend_w = 190
    legend_h = _LEGEND_PAD * 2 + len(items) * _LEGEND_ITEM_H
    x0 = screen.get_width() - legend_w - 5
    y0 = 5

    bg = pygame.Surface((legend_w, legend_h), pygame.SRCALPHA)
    bg.fill(_PANEL_BG)
    screen.blit(bg, (x0, y0))

    for i, (color, label) in enumerate(items):
        iy = y0 + _LEGEND_PAD + i * _LEGEND_ITEM_H
        pygame.draw.rect(screen, color,
                         (x0 + _LEGEND_PAD, iy + 2, _LEGEND_SWATCH, _LEGEND_SWATCH))
        text = font.render(label, True, (230, 230, 230))
        screen.blit(text, (x0 + _LEGEND_PAD + _LEGEND_SWATCH + 6, iy + 3))


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            return False
    return True
