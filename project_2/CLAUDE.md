# Project 2: Connect 4 Adversarial Search

# Description
This project implements a Connect 4 game driven by adversarial search. The program supports two modes: a human player vs an AI agent, and an AI agent vs AI agent (both sides using the same algorithm). The AI is built on Minimax search with Alpha-Beta pruning and Iterative Deepening. The game is visualized in real time using pygame, showing the board state after each move is played.

# Repo
The solution is built in Python. Source files live in the `src/` directory, each exposed as its own module. The layout mirrors project_1:
- `main.py`        — entry point, argument parsing, game loop
- `board.py`       — Connect 4 board state, move application, win/draw detection
- `minimax.py`     — Minimax with Alpha-Beta pruning and Iterative Deepening
- `heuristic.py`   — static board evaluation function used by Minimax
- `visualization.py` — all pygame drawing logic

# Style Guide
All code follows the Python 3 standard. Whitespace rules follow the configuration in `~/.vimrc` and `~/.config/nvim/init.lua`.

# CLI Arguments
The program is invoked from the command line with the following arguments:
```
python src/main.py --mode <mode> --depth <depth>
```
- `--mode`   required; choices: `ai_vs_human`, `ai_vs_ai`
- `--depth`  required; integer; the maximum lookahead depth (difficulty) passed to the Minimax search

In `ai_vs_human` mode the human plays as Red and always moves first. The AI plays as Yellow.
In `ai_vs_ai` mode both agents use the same algorithm and the same `--depth` value. Red moves first.

# Board
Connect 4 is played on a 6-row × 7-column grid. Discs fall to the lowest available row in the chosen column (gravity). A player wins by connecting 4 of their discs in a row horizontally, vertically, or diagonally. The game ends in a draw if all 42 cells are filled with no winner.

Cell values:
- `0` — empty
- `1` — Red (human in ai_vs_human, first agent in ai_vs_ai)
- `2` — Blue (AI in ai_vs_human, second agent in ai_vs_ai)

The board is represented internally as a 2D list of integers (6 rows × 7 cols), row 0 is the top.

# Algorithms
The adversarial search details are fully specified in the per-task instruction files under `tasks/`. At a high level:
- **Minimax** — standard two-player zero-sum tree search; the AI maximizes its heuristic score, the human/opponent minimizes it
- **Alpha-Beta Pruning** — added to Minimax to prune branches that cannot affect the outcome, reducing the effective search space
- **Iterative Deepening** — the search is run repeatedly from depth 1 up to `--depth`, using the result of each shallower pass to inform move ordering for the next, improving pruning efficiency. The best move from the final completed depth is played.

# Heuristic
The static evaluation function scores a board position from the perspective of the maximizing player. Details are specified in the heuristic task file. It should run in O(rows × cols) time since it is called at every leaf node of the search tree.

# Visualization
The pygame window displays the Connect 4 board as a 6×7 grid. Each cell is a colored circle drawn over a dark blue rectangular backing:
- Empty cell   — dark background circle (slot appearance)
- Red disc     — red filled circle
- Blue disc   — blue filled circle

The board is redrawn and `pygame.display.flip()` is called after every move. The human player selects a column by clicking anywhere in that column with the mouse (`MOUSEBUTTONDOWN`). A column-hover highlight may be drawn to indicate which column the mouse is over.

The same WSL2 audio fix from project_1 must be present at the top of `visualization.py`:
```python
os.environ['SDL_AUDIODRIVER'] = 'dummy'
```

# End State Display
When the game ends (win or draw), a centered text overlay is drawn on top of the board using `pygame.font.SysFont`. The message is:
- `"Red Wins"`    — if Red connects 4
- `"Blue Wins"`   — if Blue connects 4
- `"Draw"`        — if the board is full with no winner

The window stays open until the user presses any key or closes it, using the same `handle_events` / `pygame.time.wait(16)` pattern from project_1.

# Output
There is no file output. All output is the pygame window. Terminal stdout may be used for debug logging during development but is not part of the final deliverable.
