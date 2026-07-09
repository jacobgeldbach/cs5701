# Task: Map Terrain Generation program, Constraint Satisfaction Problem

# Context: Look in directory ../project_1. That was a project where using the different search alogirthms and with 40x40 grid maps as input with different cost terrains. This project is going to do the opposite using min-conflicts local search algorithm this project will generate different terrain maps that satisfy all of the different terrains and adjacency restraints that will be defined later in this file. Make sure to build your context window using the .md in the root of ../project_1. I want to use the same pygame visualization library that is described in the ../project_1 and ../project_2 projects .md files. Each terrain cell will be defined by an interger in a 2D list. As the constaint is related to adjacency based on that integer value to be described later.

# Terrains:
Six terrain types are used in this project, ordered from lowest to highest elevation:

Symbol  Terrain     Notes                                   integer value (elevation)
W Water Open water; lowest elevation                        0
B Beach Coastal sand; transitional between water and land   1
L Lowland Flat open terrain; fields and plains              2
F Forest Forested terrain; moderate elevation               3
H Hills Rolling hills; elevated terrain                     4
M Mountains High peaks; highest elevation                   5

# Adjacency rule: Two terrain types may be placed next to each other if and only if they are neighbors in the ordering above — that is, their positions in the sequence differ by at most 1. For example, Beach may be adjacent to Water or Lowland, but not Forest, Hills, or Mountains.


# Neighbors and diagonal adjacency:
Each cell has either 4 neighbors (up, down, left, right) or 8 neighbors (including the four diagonals), depending on experimental condition. The grid does not wrap — cells at the edges and corners have fewer neighbors accordingly.
Including diagonal neighbors significantly increases the number of constraint edges in the graph, which affects both the difficulty of finding a solution and the rate of convergence. You will run experiments with diagonals both enabled and disabled so this will be a command line argument.
Note: In this project, adjacency constraints apply to immediately neighboring cells. In other applications of spatial CSPs, constraints are sometimes applied to cells within a larger neighborhood radius (e.g., no two mountains within 3 cells of each other). This can produce qualitatively different map textures and is worth considering if you pursue the extra credit extension.
