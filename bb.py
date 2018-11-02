import numpy as np
import heapq
from nodefun import Node
import time


def set_dig_inf(matrix):
    matrix = matrix.astype('float')
    for i in range(matrix.shape[0]):
        matrix[i][i] = np.Inf
    return matrix


def LCBB(matrix):
    live_nodes = []
    root = Node(matrix, 0, [], -1, 0)
    heapq.heappush(live_nodes, (root.lower_bound, root))

    while(len(live_nodes) != 0):
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

def parseArr(s):
    ar = []
    line = s.split()
    for n in line:
        if n != '':
            ar.append(int(n))
    return np.array(ar)


def read_matrix(filename):
    with open(filename) as f:
       # nrows = int(f.readline())
        next(f)
        matrix = np.array(parseArr(f.readline()))
        for line in f.readlines():
            linearr = parseArr(line)
            matrix = np.vstack([matrix, linearr])
    return matrix


if __name__ == '__main__':
    matrix = read_matrix(filename='test/15_test.txt')
    m = set_dig_inf(matrix)
    start = time.time()
    tour, cost = LCBB(m)
    end = time.time()
    print(f'min cost = {cost}')
    print(0, end=" ")
    for edge in tour:
        print(edge[1], end=" ")
    print()
    print(f'Time = {end-start}')
