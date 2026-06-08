import os
import pygame
from map import Terrain

# Make pygame audio driver warnings go away, essentially giving it a dummy audio driver instead of it trying to initialize the real one 
os.environ['SDL_AUDIODRIVER'] = 'dummy'

CELL_SIZE   = 22
_GAP        = 1
_SLOT       = CELL_SIZE + _GAP
_GRID_SIZE  = 40
_WIN_SIZE   = _GRID_SIZE * _SLOT + _GAP
_SEPARATOR    = (50, 50, 50)
_LEGEND_W      = 248
_LEGEND_H      = 117
_LEGEND_PAD    = 9
_LEGEND_ITEM_H = 30
_LEGEND_SWATCH = 20

_BASE_COLOR = {
    Terrain.ROAD:      (180, 180, 180),
    Terrain.FIELD:     (210, 210, 210),
    Terrain.FOREST:    ( 34, 100,  34),
    Terrain.HILLS:     (160, 130,  80),
    Terrain.MOUNTAINS: (101,  67,  33),
    Terrain.WATER:     ( 30, 100, 200),
    Terrain.START:     (  0, 220,  50),
    Terrain.END:       (220,  50,  50),
}


def cell_color(terrain: Terrain, darkened: bool = False) -> tuple[int, int, int]:
    color = _BASE_COLOR[terrain]
    if darkened:
        return tuple(int(c * 0.55) for c in color)
    return color

# Initialize the pygame "screen" and draw its initial state
def init_display(grid: list) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((_WIN_SIZE, _WIN_SIZE))
    pygame.display.set_caption('Pathfinding Visualization')
    draw_grid(screen, grid)
    pygame.display.flip()
    return screen

# Using the pygame library, draw the 40x40 cell static map that has been read in 
def draw_grid(screen: pygame.Surface, grid: list) -> None:
    screen.fill(_SEPARATOR)
    for row in range(_GRID_SIZE):
        for col in range(_GRID_SIZE):
            cell = grid[row][col]
            color = _BASE_COLOR[cell.type]
            x = col * _SLOT + _GAP
            y = row * _SLOT + _GAP
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

# As opposed to draw_grid which is called once, this is called per algorithm step to visualize the current OpenList and ClosedList in real time
def draw_overlay(
    screen: pygame.Surface,
    open_set: set,
    closed_set: set,
) -> None:
    closed_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    closed_surf.fill((50, 100, 220, 80))
    open_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    open_surf.fill((50, 200, 50, 80))

    for (row, col) in closed_set:
        x = col * _SLOT + _GAP
        y = row * _SLOT + _GAP
        screen.blit(closed_surf, (x, y))

    for (row, col) in open_set:
        x = col * _SLOT + _GAP
        y = row * _SLOT + _GAP
        screen.blit(open_surf, (x, y))

    draw_legend(screen)

def draw_legend(screen: pygame.Surface) -> None:
    font = pygame.font.SysFont('monospace', 16)
    x0 = _WIN_SIZE - _LEGEND_W - 5
    y0 = 5

    bg = pygame.Surface((_LEGEND_W, _LEGEND_H), pygame.SRCALPHA)
    bg.fill((20, 20, 20, 210))
    screen.blit(bg, (x0, y0))

    items = [
        ((50,  200,  50), 'Open List (Seen)'),
        ((50,  100, 220), 'Closed List (Explored)'),
        ((220,  30,  30), 'Solution Path'),
    ]
    for i, (color, label) in enumerate(items):
        iy = y0 + _LEGEND_PAD + i * _LEGEND_ITEM_H
        pygame.draw.rect(screen, color,
                         (x0 + _LEGEND_PAD, iy + 2, _LEGEND_SWATCH, _LEGEND_SWATCH))
        text = font.render(label, True, (230, 230, 230))
        screen.blit(text, (x0 + _LEGEND_PAD + _LEGEND_SWATCH + 5, iy + 2))

# Once the End cell has been found, this draws the path of cells back to Start Cell red
def draw_path(screen: pygame.Surface, path: list) -> None:
    path_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    path_surf.fill((220, 30, 30, 190))

    for cell in path:
        x = cell.col * _SLOT + _GAP
        y = cell.row * _SLOT + _GAP
        screen.blit(path_surf, (x, y))

    draw_legend(screen)


def handle_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            return False
    return True
