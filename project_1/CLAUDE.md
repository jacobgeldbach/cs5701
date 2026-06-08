# Project 1: Pathfinding

# Description: This project I am tasked with implementing 5 different (really 4) search algorithms, where a suite of 3 different test maps will have the search algorithms ran against them with the goal of 1) visualizing the search algorithms via some sort of graphics display and 2) collection of quantitive data that relates to the alorithms that will be defined and detailed in later context sections and in later tasks.

# Repo: The solution will be built in Python, each algorithm will have its own src file in the src/ directory and will be exposed as its own module. There will also be specific src files for the main function of the project and for the graphics driving module that imports the needed graphics libraries.

# Style Guide: The style of all written code in this project will follow the Python3 standard, and whitespace rules will follow all the configuration found in .vimrc and my nvim init.lua found here /home/geldbach/.config/nvim/init.lua.

# Input: The only input to this program will be the plain-text file "Maps" where each "cell" is an ascii character. These "Map" text files will be read by the program at runtime.

# Maps: There will only be 3 Maps that will be used as input for each of the 5 alorithms. Each Map is a 40x40 cell plain-text file. Each line of the map is one row of the grid. Each cell will be read left to right and top to bottom. There are no spaces or delimiters between the cells. And each cell will be an ascii character describing a "Terrain" with a key as follows:
Symbol|Terrain    |Move Cost   |Notes
R      Road        1            Fastest movement; minimal resistance
F      Field       3            Open ground; default terrain
O      Forest      5            Dense vegetation slows movement
H      Hills       8            Elevated terrain; significantly slower
M      Mountains   15           Very difficult; high cost but passable
W      Water       —            Impassable (lakes only; no rivers)
S      Start       —            Agent start position
E      End         —            Goal position

# Cells: Each cell when read in will be represented by a unified cell or node struct. It will container fields detailing the type of terrain, cost and a pointer to the previous cell so the path to get to that cell is preserved. This unified cell data-structure will be further defined later in the map input read and initial cell processing implementation task.

# Algorithms: The algorithm at runtime will have the ability to move either up or down or left or right from its current cell, it is not allowed to move diagnonally from cell to cell. The cost of the agents movement is incurred at the time of entering of the destination cell as defined in the key from the previous "Maps" context section. The algorithms will be implemented using OpenLists and ClosedLists as their main space/state tracking data-structure, but that will be defined further in each algorithms instruction file for that specific implementation task. The details of the algorithms themselve will be defined in later per implemenation context instruction files. The names of the 5 algorithms are as follows:
    1) Breadth First Search
    2) Uniform Cost Search
    3) Greedy Best-First Search
    4) A* Search with Heuristic 1
    5) A* Search with Heuristic 2
The 2 different Heuristics for the A* searches will be defined later in those specific implementation tasks.

# Output: The output of this program will be the runtime visualization of the algorithm running and interesting analytic data specific to that ran algorithm. This analytic data will be harvest at runtime of the algorithm and will be further specified on later on during the per algorithm implementation task instructions. The analytic data types will most likely be shared between algorithm for proper comparison in my project write up when comparing the performance of the 5 algorithms.

# Visualization: The visualization will be displayed via some later to be determined Python graphics library that produces a 40x40 cell grid where each cell is color coated to show the type of terrain that cell represents. Also the start and end goal cells will be represented by a different color. The cells not yet explored (OpenList cells) and the already explored cells (ClosedList cells) will be differentiated in the visualization while algorithm is running. Once the algorithm has reached a goal state, and a path from start to end has been determined via the algorithm, the path will be drawn clearly over the visualization from start cell to end cell.
