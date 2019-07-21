import numpy as np
import time
from bb import LCBB
from simulated_annealing import SimulatedAnnealing
from utils import read_matrix, calc_tour_length, set_dig_inf
import itertools


class TSP:
    def __init__(self, dist_matrix=None, filename=None):
        self.dist_matrix = dist_matrix
        self.minTour = []
        self.tourLength = np.Inf
        if filename is not None:
            self.dist_matrix = read_matrix(filename)

    def Brute_Force(self):
        size = self.dist_matrix.shape[0]
        for tour in itertools.permutations(range(1, size)):
            length = calc_tour_length(tour, self.dist_matrix)
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
    tsp.BranchAndBound()
    end = time.time()
    tsp.print_result()
    perfom_time = end - start
    print("time: ", perfom_time)
