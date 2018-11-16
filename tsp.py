import numpy as np
import time
from bb import LCBB, set_dig_inf


class TSP:
    def __init__(self, dist_matrix=None, filename=None):
        self.dist_matrix = dist_matrix
        self.minTour = []
        self.tourLength = np.Inf
        if filename is not None:
            self.read_matrix(filename)

    @staticmethod
    def parseArr(s):
        arr = []
        line = s.split()
        arr = [int(n) for n in line if n != '']
        return np.array(arr)

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

    def read_matrix(self, filename):
        with open(filename) as f:
           # nrows = int(f.readline())
            next(f)
            matrix = np.array(TSP.parseArr(f.readline()))
            for line in f.readlines():
                linearr = TSP.parseArr(line)
                matrix = np.vstack([matrix, linearr])
        self.dist_matrix = matrix

    def set_dig_inf(matrix):
        matrix = matrix.astype('float')
        for i in range(matrix.shape[0]):
            matrix[i][i] = np.Inf
        return matrix


if __name__ == '__main__':
    tsp = TSP(filename='test/13_test.txt')
    start = time.time()
    tsp.Brute_Force()
    end = time.time()
    tsp.print_result()
    perfom_time = end - start
    print("time: ", perfom_time)
