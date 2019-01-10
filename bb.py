import numpy as np
import heapq
from node import Node


def set_dig_inf(matrix):
    matrix = matrix.astype('float')
    for i in range(matrix.shape[0]):
        matrix[i][i] = np.Inf
    return matrix


def LCBB(matrix):
    live_nodes = []
    root = Node(matrix, 0, [], -1, 0)
    heapq.heappush(live_nodes, (root.lower_bound, root))

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
