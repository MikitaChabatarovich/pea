import numpy as np
import heapq
from node import Node
import time


def infinity_diagonal(matrix):
    matrix = matrix.astype('float')  # ??
    for i in range(matrix.shape[0]):
        matrix[i][i] = np.Inf
    return matrix


def LCBB(matrix):
    live_nodes = []
    root = Node(matrix, 0, [], -1, 0)
    heapq.heappush(live_nodes, (root.lower_bound, root))
    upper_bound = np.Inf

    while live_nodes:
        curr_node = heapq.heappop(live_nodes)[1]
        curr_city = curr_node.city

        if curr_node.level == matrix.shape[0] - 1:
            curr_node.tour.append((curr_city, 0))
            tour = curr_node.tour
            return tour, curr_node.lower_bound

        for i in range(matrix.shape[0]):
            if(curr_node.reduced_matrix[curr_city][i] != np.Inf):
                newNode = Node(curr_node.reduced_matrix, curr_node.level + 1,
                               curr_node.tour, curr_city, i, curr_node.lower_bound)
                heapq.heappush(live_nodes, (newNode.lower_bound, newNode))


class BranchAndBound:
    def __init__(self):
        self.final_path = None
        self.final_cost = None
        self.costs_matrix = None
        self.upper_bound = np.Inf

    @staticmethod
    def compute_lower_bound(node):
        cost = node.reduced_matrix[node.from_city][node.city]
        rows_cols_min = node.reduce_martix()
        reduction_cost = sum(rows_cols_min)
        if node.level == 0:
            return reduction_cost
        return reduction_cost + node.p_lb + cost

    def solve(self, matrix):
        self.costs_matrix = infinity_diagonal(matrix)
        live_nodes = []
        root = Node(self.costs_matrix)
        root.lower_bound = BranchAndBound.compute_lower_bound(root)
        heapq.heappush(live_nodes, root)

        while live_nodes:
            node = heapq.heappop(live_nodes)

            if node.level == matrix.shape[0] - 1:
                node.tour.append((node.city, 0))
                tour = node.tour
                # return tour, node.lower_bound
                self.final_path = node.tour

            for i in range(matrix.shape[0]):
                if(node.reduced_matrix[node.city][i] != np.Inf):
                    new_node = Node(reduced_matrix=node.reduced_matrix,
                                    level=node.level + 1,
                                    p_tour=node.tour,
                                    fr=node.city,
                                    to=i,
                                    p_lb=node.lower_bound)

                    new_node.lower_bound = BranchAndBound.compute_lower_bound(new_node)
                    heapq.heappush(live_nodes, new_node)
