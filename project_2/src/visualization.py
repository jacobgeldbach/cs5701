import os
import pygame

os.environ['SDL_AUDIODRIVER'] = 'dummy'

_COLS      = 7
_ROWS      = 6
_CELL_SIZE = 100
_GAP       = 10
_SLOT      = _CELL_SIZE + _GAP
_RADIUS    = _CELL_SIZE // 2 - 3

_STATUS_H  = 48
_GHOST_H   = _SLOT
_BOARD_H   = _ROWS * _SLOT + _GAP
_WIN_W     = _COLS * _SLOT + _GAP
_WIN_H     = _STATUS_H + _GHOST_H + _BOARD_H
_BOARD_Y   = _STATUS_H + _GHOST_H

_BOARD_BG   = ( 30,  80, 160)
_EMPTY_SLOT = ( 15,  15,  45)
_STATUS_BG  = ( 20,  20,  45)

_PLAYER_COLOR = {
    1: (220,  50,  50),
    2: ( 50, 120, 220),
}
_PLAYER_LABEL = {
    1: 'Red',
    2: 'Blue',
}


def _cell_center(row: int, col: int) -> tuple[int, int]:
    x = _GAP + col * _SLOT + _CELL_SIZE // 2
    y = _BOARD_Y + _GAP + row * _SLOT + _CELL_SIZE // 2
    return x, y


def _ghost_center(col: int) -> tuple[int, int]:
    x = _GAP + col * _SLOT + _CELL_SIZE // 2
    y = _STATUS_H + _GAP + _CELL_SIZE // 2
    return x, y


def mouse_to_col(x: int) -> int | None:
    col = x // _SLOT
    if 0 <= col < _COLS:
        return col
    return None


def init_display() -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((_WIN_W, _WIN_H))
    pygame.display.set_caption('Connect 4')
    return screen


def draw_board(screen: pygame.Surface, board: list) -> None:
    pygame.draw.rect(screen, _BOARD_BG, (0, _BOARD_Y, _WIN_W, _BOARD_H))
    for row in range(_ROWS):
        for col in range(_COLS):
            cx, cy = _cell_center(row, col)
            val = board[row][col]
            color = _PLAYER_COLOR.get(val, _EMPTY_SLOT)
            pygame.draw.circle(screen, color, (cx, cy), _RADIUS)


def draw_ghost(screen: pygame.Surface, col: int | None, player: int) -> None:
    pygame.draw.rect(screen, _BOARD_BG, (0, _STATUS_H, _WIN_W, _GHOST_H))
    if col is None or not (0 <= col < _COLS):
        return
    cx, cy = _ghost_center(col)
    base = _PLAYER_COLOR[player]
    ghost_surf = pygame.Surface((_CELL_SIZE, _CELL_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(ghost_surf, (*base, 140), (_CELL_SIZE // 2, _CELL_SIZE // 2), _RADIUS)
    screen.blit(ghost_surf, (cx - _CELL_SIZE // 2, cy - _CELL_SIZE // 2))


def draw_status(screen: pygame.Surface, text: str, player: int | None = None) -> None:
    pygame.draw.rect(screen, _STATUS_BG, (0, 0, _WIN_W, _STATUS_H))
    font = pygame.font.SysFont('monospace', 26)
    color = _PLAYER_COLOR.get(player, (230, 230, 230))
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(_WIN_W // 2, _STATUS_H // 2))
    screen.blit(surf, rect)


def draw_end_overlay(screen: pygame.Surface, message: str) -> None:
    overlay = pygame.Surface((_WIN_W, _WIN_H), pygame.SRCALPHA)
    overlay.fill((10, 10, 30, 180))
    screen.blit(overlay, (0, 0))
    font = pygame.font.SysFont('monospace', 56, bold=True)
    if 'Red' in message:
        color = _PLAYER_COLOR[1]
    elif 'Blue' in message:
        color = _PLAYER_COLOR[2]
    else:
        color = (230, 230, 230)
    surf = font.render(message, True, color)
    rect = surf.get_rect(center=(_WIN_W // 2, _WIN_H // 2))
    screen.blit(surf, rect)


def handle_events() -> tuple[bool, int | None]:
    clicked_col = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and clicked_col is None:
            clicked_col = mouse_to_col(event.pos[0])
    return True, clicked_col


def handle_end_events() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            return False
    return True
