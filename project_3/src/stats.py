from dataclasses import dataclass


@dataclass
class GenerationStats:
    rows:            int
    cols:            int
    diagonals:       bool
    steps:           int
    restarts:        int
    initial_conflicts: int
    final_conflicts: int
    solved:          bool
    runtime:         float

    def __str__(self) -> str:
        neighbors = 8 if self.diagonals else 4
        return (
            f"  Grid              : {self.rows}x{self.cols} ({neighbors}-neighbor)\n"
            f"  Solved            : {self.solved}\n"
            f"  Steps             : {self.steps}\n"
            f"  Restarts          : {self.restarts}\n"
            f"  Initial conflicts : {self.initial_conflicts}\n"
            f"  Final conflicts   : {self.final_conflicts}\n"
            f"  Runtime           : {self.runtime:.4f}s"
        )
