# Task 5: Implement the Greedy Best First Algorithm

# Context: This will be the first Informed Global Search algorithm that is implemented in this project. Meaning a heuristic will need to be used. This heuristic will be defined later in this context file. The visualization of this algorithm will be the exact same as the previous two algorithms and the algorithm itself will also be defined in detail below. There will be a new command line argument added --gbfs.

# Heuristic: The heuristic used will be the cost from that specific cell to the End cell. This will need to be stored in a dictionary that maps the cells coordinates in a tuple to an integer which is that cost to End cell. In order to produce this dictionary the algorithm will use for the heuristic the UCS algorithm must be used on each cell after the initial map is read in and the 40x40 grid is built. There will be a new parameter added to the algorithm functions (bfs() and ucs()) that specify the amount of ms to sleep between iterations. That way when generating this heuristic dictionary for each cell, it can be called per cell with a sleep between iteration of 0ms (ucs(0) that way this section of the program exectues much faster since the sleep is only there for the overlay visualization. Also null will need to be passed into the ucs() function per cell in place of the pygame screen as the visualization of the per cell heuristic dictionary building stage is not needed. With that paramter being null the pygame related visualization drawing per step will be skipped. Once the heuristic dictionary is built the main call of the greedy best first function will be called. The heuristic building will be done no matter which --algo argument is passed as the remaining algorithms will require a heuristic as well.

# Greedy Best First Search Algorithm:
Add the Start cell to the OpenList
Begin loop
    Remove the next state from the OpenList (Next is defined as the front of the OpenList)
    If cell node is the End cell
        return the End node and therefore its Path to back to the start cell
    else
        Add the cell node to the ClosedList
        add all neighboring cells not on the ClosedList to the OpenList
        Remove Duplicates
    Sort the OpenList by the heuristic of cost to reach the End cell
Back to start of loop
