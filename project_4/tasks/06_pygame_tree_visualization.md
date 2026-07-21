# Task 6: visualization.py — pygame decision tree renderer

# Context: Renders one built decision tree (a tree.py Node) as a pygame window, similar
in spirit to the pygame visualizations in project_1/project_2 (same WSL2 audio fix at
the top of the file: os.environ['SDL_AUDIODRIVER'] = 'dummy' before importing pygame).
This is a static diagram (no animation/search-step overlay needed here, unlike
project_1) — it draws once and stays open until the window is closed or a key pressed.

# Layout: Compute node positions with a simple level-order (BFS) layout:
- depth (root = level 0) determines the y-coordinate band.
- within a level, assign x-coordinates left-to-right in the order nodes are
  encountered via an in-order-ish traversal (children of a node placed adjacent to
  each other, centered under their parent) so the tree reads left-to-right/top-to-
  bottom without overlapping boxes. A simple recursive approach: compute each leaf's
  x slot first (leaves get sequential slots), then each internal node's x is the
  average of its two children's x.

# Drawing:
- Internal (attribute) nodes: rounded rectangle box, light blue fill, attribute name
  text centered inside (e.g. "In a hurry").
- Leaf nodes: rounded rectangle box, colored by predicted label — green fill for
  "Yes" (ask for help), orange/red fill for "No" (robot decides) — with the label text
  centered inside.
- Edges: a line from parent box to each child box, labeled "0" near the 0-branch line
  and "1" near the 1-branch line (or "No"/"Yes" if that reads more clearly — pick one
  and be consistent).
- Window title should include the training set size used to build the tree, e.g.
  "Decision Tree (trained on 20 examples)".

# Function: show_tree(root, attributes, train_size=None) — opens the pygame window,
draws the tree once via the layout above, then loops calling pygame.time.wait(16) and
handling QUIT/KEYDOWN events until the user closes the window (same handle_events /
wait(16) idle-loop pattern as project_2).
