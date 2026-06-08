import argparse
import pygame
import copy
import random
from board import Board
from visualization import (
    init_display, draw_board, draw_ghost, draw_status,
    draw_end_overlay, handle_events, handle_end_events, mouse_to_col,
)
from minimax import mini_max 

_PLAYER_NAME = {1: 'Red', 2: 'Blue'}


def _wait(ms: int) -> bool:
    elapsed = 0
    while elapsed < ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.time.wait(16)
        elapsed += 16
    return True


def _end_screen(screen, message: str) -> None:
    draw_end_overlay(screen, message)
    pygame.display.flip()
    while handle_end_events():
        pygame.time.wait(16)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', required=True, choices=['ai_vs_human', 'ai_vs_ai'])
    parser.add_argument('--depth', required=True, type=int)
    args = parser.parse_args()

    board = Board()
    screen = init_display()
    current = random.choice([1, 2])
    hover_col = None
    running = True

    while running:
        human_turn = (args.mode == 'ai_vs_human' and current == 1)

        draw_status(screen, f"{_PLAYER_NAME[current]}'s Turn", current)
        draw_ghost(screen, hover_col if human_turn else None, current)
        draw_board(screen, board.grid)
        pygame.display.flip()

        if human_turn:
            running, clicked_col = handle_events()
            hover_col = mouse_to_col(pygame.mouse.get_pos()[0])

            if not running:
                break
            if clicked_col is None or not board.is_valid_col(clicked_col):
                pygame.time.wait(16)
                continue
            col = clicked_col
        else:
            running = _wait(400)
            if not running:
                break
            col = mini_max(copy.deepcopy(board), args.depth, current)

        board.drop_piece(col, current)
        draw_status(screen, f"{_PLAYER_NAME[current]}'s Turn", current)
        draw_ghost(screen, None, current)
        draw_board(screen, board.grid)
        pygame.display.flip()

        if board.check_win(current):
            _end_screen(screen, f"{_PLAYER_NAME[current]} Wins")
            break
        if board.is_draw():
            _end_screen(screen, "Draw")
            break

        current = 2 if current == 1 else 1
        if human_turn:
            hover_col = None

    pygame.quit()


if __name__ == '__main__':
    main()
