import argparse
import pygame
from map import map_read_process
from heuristic import build_heuristic, MANHATTAN, AVG_WEIGHTED_MANHATTAN, REVERSED_UCS
from visualization import init_display, handle_events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--map',  required=True)
    parser.add_argument('--algo', choices=['bfs', 'ucs', 'gbfs', 'astar'], required=True)
    parser.add_argument(
        '--heuristic',
        choices=['man', 'weight_man', 'reversed_ucs'],
        default='man',
    )
    args = parser.parse_args()

    _HEURISTIC_MAP = {
        'man':          MANHATTAN,
        'weight_man':   AVG_WEIGHTED_MANHATTAN,
        'reversed_ucs': REVERSED_UCS,
    }

    grid, start_row, start_col, end_row, end_col = map_read_process(args.map)
    
    if args.heuristic != None:
        heuristic = build_heuristic(grid, end_row, end_col, method=_HEURISTIC_MAP[args.heuristic])

    screen = init_display(grid)

    algo = args.algo.lower()

    if algo == 'bfs':
        from bfs import bfs
        stats = bfs(grid, start_row, start_col, screen)
        print(f"\nBFS Results:\n{stats}")
    elif algo == 'ucs':
        from ucs import ucs
        stats = ucs(grid, start_row, start_col, screen)
        print(f"\nUCS Results:\n{stats}")
    elif algo == 'gbfs':
        from gbfs import gbfs
        stats = gbfs(grid, start_row, start_col, screen, heuristic)
        print(f"\nGBFS Results:\n{stats}")
    elif algo == 'astar':
        from astar import astar
        stats = astar(grid, start_row, start_col, screen, heuristic)
        print(f"\nA* Results:\n{stats}")

    while handle_events():
        pygame.time.wait(16)
    pygame.quit()


if __name__ == '__main__':
    main()
