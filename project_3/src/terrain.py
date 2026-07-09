# Terrain integer values, ordered lowest to highest elevation (see map_terrain.md).
# A generated map is a 2D list of these ints; two adjacent cells are legal iff
# their values differ by at most 1.
WATER     = 0
BEACH     = 1
LOWLAND   = 2
FOREST    = 3
HILLS     = 4
MOUNTAINS = 5

NUM_TERRAINS = 6

NAME = {
    WATER:     'Water',
    BEACH:     'Beach',
    LOWLAND:   'Lowland',
    FOREST:    'Forest',
    HILLS:     'Hills',
    MOUNTAINS: 'Mountains',
}

SYMBOL = {
    WATER:     'W',
    BEACH:     'B',
    LOWLAND:   'L',
    FOREST:    'F',
    HILLS:     'H',
    MOUNTAINS: 'M',
}
