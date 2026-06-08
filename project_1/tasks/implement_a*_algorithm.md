# Task 6: Implement the A* algorithm

# Context: The final algorithm for implementation is the A* algorithm. The algorithm will be defined in detail below. It will also use whatever heuristic is built into the heuristic dictionary at time of run based on the --heuristic argument. All visualization requirements will be the same as the other algorithms. This algorithm will take advantage of the g_cost dictionary as it will require the cost to get to a cell + the heuristic value for that cell.

# A*:
Add the Start cell to the OpenList
Begin loop
    Remove the next state from the OpenList (Next is defined as the front of the OpenList)
    If cell node is the End cell
        return the End node and therefore its Path to back to the start cell
    else
        Add the cell node to the ClosedList
        add all neighboring cells not on the ClosedList to the OpenList
        Remove Duplicates
    Sort the OpenList by its g_cost (cost to reach) + heuristic value for that cell (estimated cost to End cell)
Back to start of loop
