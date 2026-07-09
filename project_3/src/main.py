import argparse
import random
import pygame
import terrain
from min_conflicts import min_conflicts
from visualization import init_display, handle_events


# Square grid dimension for each --size index, smallest (0) to largest (4).
_SIZES = [50, 75, 100, 150, 200]


# Build a complete random assignment of terrains. min-conflicts starts from a
# fully-assigned (typically conflicting) grid and then repairs it, so a random
# fill is exactly the right starting state.
def make_random_grid(rows: int, cols: int) -> list[list[int]]:
    return [[random.randrange(terrain.NUM_TERRAINS) for _ in range(cols)] for _ in range(rows)]


def main():
    parser = argparse.ArgumentParser(
        description='Terrain map generation via min-conflicts local search (CSP)'
    )
    parser.add_argument('--size', type=int, default=0, choices=range(len(_SIZES)),
                        help='grid size index: 0=50, 1=75, 2=100, 3=150, 4=200')
    parser.add_argument('--diagonals', action='store_true',
                        help='use 8-neighbor adjacency (4-neighbor when omitted)')
    parser.add_argument('--max-steps', type=int, default=15000,
                        help='maximum min-conflicts iterations before giving up')
    parser.add_argument('--delay', type=int, default=0,
                        help='ms to wait between visualization steps (0 = full speed)')
    args = parser.parse_args()

    dim = _SIZES[args.size]
    grid = make_random_grid(dim, dim)
    screen = init_display(grid)

    stats = min_conflicts(grid, args.diagonals, args.max_steps, screen, args.delay)
    print(f"\nMin-Conflicts Results:\n{stats}")

    while handle_events():
        pygame.time.wait(16)
    pygame.quit()


if __name__ == '__main__':
    main()
