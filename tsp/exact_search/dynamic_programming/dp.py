from functools import lru_cache

_matrix = None


@lru_cache(maxsize=512)
def dist(from_, to):
    return _matrix[from_][to]


def C(S, i):
    if len(S) == 1:
        end_node = list(S)[0]
        return dist(i, end_node) + dist(end_node, 0)
    else:
        return min([C(S - {i, j}, j) + dist(i, j) for j in S])


def solve(matrix, size):
    global _matrix
    _matrix = matrix
    v = set(range(1, size))
    return C(v, 0)
