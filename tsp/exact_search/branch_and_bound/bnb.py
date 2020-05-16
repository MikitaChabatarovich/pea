import gc
import numpy as np
import heapq
from .node import Node
from utils import infinity_diagonal


class BranchAndBound:
    def __init__(self):
        self.final_path = None
        self.final_cost = None
        self.costs_matrix = None

    def solve(self, matrix):
        self.costs_matrix = infinity_diagonal(matrix)
        live_nodes = []
        root = Node(self.costs_matrix)
        heapq.heappush(live_nodes, root)

        while live_nodes:
            node = heapq.heappop(live_nodes)

            if node.level == matrix.shape[0] - 1:
                node.tour.append((node.city, 0))
                self.final_path = [edge[1] for edge in node.tour][:-1]
                self.final_cost = int(node.lower_bound)
                return

            for i in range(matrix.shape[0]):
                if(node.reduced_matrix[node.city][i] != np.Inf):
                    new_node = Node(
                        reduced_matrix=node.reduced_matrix,
                        level=node.level + 1,
                        p_tour=node.tour,
                        fr=node.city,
                        to=i,
                        p_lb=node.lower_bound
                    )

                    heapq.heappush(live_nodes, new_node)
            del node
            gc.collect()  # 95% less memory 120% slower
