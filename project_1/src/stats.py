from dataclasses import dataclass


@dataclass
class SearchStats:
    nodes_expanded:   int
    nodes_seen:       int
    states_remaining: int
    path_length:      int
    path_cost:        int
    runtime:          float

    def __str__(self) -> str:
        return (
            f"  Nodes expanded    : {self.nodes_expanded}\n"
            f"  Nodes seen        : {self.nodes_seen}\n"
            f"  States remaining  : {self.states_remaining}\n"
            f"  Path length       : {self.path_length} cells\n"
            f"  Path cost         : {self.path_cost}\n"
            f"  Runtime           : {self.runtime:.4f}s"
        )
