# Task 3: Implement the first search algorithm Breadth First Search

# Context: Implement a classic Breadth First Search algorithm that begins at the Start Cell and continues until the End Cell is found. The exact algorithm to be implemented will be defined in detail below. This is an uninformed global search so the cost of each cell will be irrelevant and the algorithm will only be optimal in regards to finding the optimal path of least actions as opposed to optimal path of least cost. The algorithm will not require any tree building, the 40x40 grid of cells that represent the map will only be used to determine the neighboring nodes to the node currently being processed. The algorithm will use an OpenList and a ClosedList as the only data structures required in order to keep state of "explored" nodes vs "seen" nodes. A seen node is one added to the OpenList, and an explored node is one removed from the OpenList and added to the ClosedList. The real time visualization of the contents of the OpenList and the ClosedList will be shown per iteration of the algorithm, by updating the 40x40 pygame map visualization per iteration by making the "seen" nodes a slightly green shade on top of their current color cell, and the "explored" nodes a slightly blue shade over their regular cell color. These two shades being see through so you can see the original color of the cell still. Once the End cell has been found (not just found but removed from the OpenList as per the below defined algorith, a red path will be traced in the final pygame visualization detailing the path the algorithm found back to the start cell. This can be acheived via the parent field in the cell struct, following the trace from cell node to cell node until the Start cell is found again. Remember that diagonal movement is NOT allowed.

# BFS Algorithm:
Add the Start cell to the OpenList
Begin loop
    Remove the next state from the OpenList (Next is defined as the front of the OpenList or the oldest cell node on the OpenList)
    If cell node is the End cell
        return the End node and therefore its Path to back to the start cell
    else
        Add the cell node to the ClosedList
        add all neighboring cells not on the ClosedList to the OpenList
Back to start of loop
