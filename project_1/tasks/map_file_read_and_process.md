# Task 1: Map file read and process

# Goal: Read in the Map input files and process each read character into a cell struct. Each cell read in needs to be stored in a 40x40 grid 2D list, since the plain-text character maps are also 40x40.

# Context: For this task create the first two src files in the src/ directory. The first being main.py and the second one being map.py. The map file to be read will be specified via a command line argument. Each character needs to be processed into a cell struct at time of that character being read and once that cell struct is built it needs to be stored in a 2D list in an index that corresponds with its index in the 40x40 plain-text ascii grid of the map file. Populate the rest of the struct based on the key given in the repo level claude.md. This should be done with a per cell struct process method that is called per Character read in. Build the main function in main.py that just calls in the map_read_process() method after retrieving the map argument from argc from the command line. The cell index that is processed as the start cell needs to be saved for when the algorithm begins. There is only need for a pointer member of 'parent' for when the algorithm begins its traversal. The algoritms will be instructed of the movement rules of up down left or right with grid boundaries so there is no need for pointers to the cells surrounding a cell in its struct.

# Cell Struct: The cell struct should be a python standard structure with fields that follow:
type: an enum of terrain start or end
cost: integer that corresponds with the cost to move to this cell
parent: pointer to the cell the explored first to get to this cell
