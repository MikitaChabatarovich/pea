import numpy as np
import time
from bb import LCBB, set_dig_inf
from simulated_annealing import SimulatedAnnealing
from utils import read_matrix

class TSP:
    def __init__(self, dist_matrix=None, filename=None):
        self.dist_matrix = dist_matrix
        self.minTour = []
        self.tourLength = np.Inf
        if filename is not None:
            self.dist_matrix = read_matrix(filename)

    @staticmethod
    def permutations(lst):
        if len(lst) == 0:
            yield []
        if len(lst) == 1:
            yield lst
        else:
            for i in range(len(lst)):
                m = lst[i]
                remLst = lst[:i] + lst[i + 1:]
                for p in TSP.permutations(remLst):
                    yield [m] + p

    def Brute_Force(self):
        size = self.dist_matrix.shape[0]
        for tour in TSP.permutations(list(range(1, size))):
            fr = 0
            length = 0
            for city in range(size - 1):
                to = tour[city]
                length += self.dist_matrix[fr][to]
                fr = to
            length += self.dist_matrix[fr][0]
            if length < self.tourLength:
                self.tourLength = length
                self.minTour = tour

    def BranchAndBound(self):
        m = set_dig_inf(self.dist_matrix)
        tour, cost = LCBB(m)
        listTour = [edge[0] for edge in tour]
        self.minTour = listTour
        self.tourLength = cost

    
    def print_result(self):
        print('Shortest tour is:', self.minTour)
        print('It has a length of:', self.tourLength, 'km')


if __name__ == '__main__':
    tsp = TSP(filename='test/6_test.txt')
    start = time.time()
    tsp.Brute_Force()
    end = time.time()
    tsp.print_result()
    perfom_time = end - start
    print("time: ", perfom_time)
