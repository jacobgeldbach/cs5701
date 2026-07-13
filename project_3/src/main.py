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
    parser.add_argument('--classic', action='store_true',
                        help='textbook min-conflicts: pick any conflicted cell at '
                             'random (default picks a most-conflicted cell)')
    parser.add_argument('--patience', type=int, default=0,
                        help='stop after this many steps without improving the best '
                             'conflict count (0 = auto: one per grid cell)')
    parser.add_argument('--max-steps', type=int, default=0,
                        help='hard safety cap on iterations (0 = no cap; patience is '
                             'the primary stopping criterion)')
    parser.add_argument('--headless', action='store_true',
                        help='run the search with no window and no drawing (fastest; '
                             'for large grids and batch experiments)')
    parser.add_argument('--delay', type=int, default=0,
                        help='ms to wait between repaints (0 = full speed)')
    args = parser.parse_args()

    dim = _SIZES[args.size]
    patience = args.patience if args.patience > 0 else dim * dim
    grid = make_random_grid(dim, dim)
    screen = None if args.headless else init_display(grid)

    stats = min_conflicts(grid, args.diagonals, patience, args.max_steps,
                          args.classic, screen, args.delay)
    print(f"\nMin-Conflicts Results:\n{stats}")

    if not args.headless:
        while handle_events():
            pygame.time.wait(16)
        pygame.quit()


if __name__ == '__main__':
    main()
