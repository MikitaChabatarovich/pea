from functools import lru_cache
from dataclasses import dataclass

_matrix = None


class Dynamic:

    def __init__(self):
        self.final_path = None
        self.final_cost = None

    def solve(self, matrix):
        _matrix_init(matrix)
        nodes_to_visit = set(range(1, len(matrix)))
        path = Path(nodes_to_visit, 0, [], 0)
        best_path = minimal_cost_path(path)
        self.final_path = best_path.path
        self.final_cost = best_path.cost


@dataclass
class Path:
    remained_nodes: set
    start_node: int
    path: list
    cost: int


@lru_cache(maxsize=1024)
def dist(from_, to):
    return _matrix[from_][to]


def minimal_cost_path(path):
    if len(path.remained_nodes) == 1:
        last_node = list(path.remained_nodes)[0]
        path.cost += dist(path.start_node, last_node) + dist(last_node, 0)
        path.path.append(last_node)
        return path
    else:
        return min([
            minimal_cost_path(_make_path(path, next_node))
            for next_node in path.remained_nodes
        ], key=lambda path: path.cost)


def _make_path(path, next_node):
    return Path(
        remained_nodes=path.remained_nodes - {path.start_node, next_node},
        start_node=next_node,
        path=path.path + [next_node],
        cost=path.cost + dist(path.start_node, next_node)
    )


def _matrix_init(matrix):
    global _matrix
    _matrix = matrix
