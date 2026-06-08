# Task 4: Implement the next search algorithm, Uniform Cost Search

# Context: Implement the next algorithm on the read in map, starting with the Start cell perform the Uniform Cost Search until the End cell is taken from the OpenList. All the same visualization instructions from the first search algorithm are in place in regards to the map drawing and overlay drawing. This algorithm will be taking into account the cost of each cell unlike the Breadth First Search. Add an argument for --algo UCS

# Uniform Cost Algorithm: The algorithm is the same as BFS, except each step after the processed cell's neighbors are added to the OpenList, the OpenList will be sorted by cost. 
