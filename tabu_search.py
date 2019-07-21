from utils import greedy_solution, read_matrix, calc_tour_length
from simulated_annealing import random_tour
import itertools
from numpy import Inf


def TabuSearch(matrix):
    pass


def best_neighbor(state, matrix):
    b_neighbor = None
    min_length = Inf
    for tour in neighors_generator(state):
        length = calc_tour_length(tour, matrix)
        if length < min_length:
            min_length = length
            b_neighbor = tour
    return b_neighbor, length


def neighors_generator(state):
    for tranform in itertools.combinations(range(len(state)), 2):
        yield make_neighor(state, tranform)


def make_neighor(state, indexes):
    neighor = list(state)
    i = indexes[0]
    j = indexes[1]
    if i > j:
        neighor[j], neighor[i] = neighor[i], neighor[j]
    else:
        neighor[i], neighor[j] = neighor[j], neighor[i]
    return neighor


if __name__ == "__main__":
    matrix = read_matrix('test/6_test.txt')
    st = random_tour(len(matrix))
    print(st, calc_tour_length(st, matrix))
    print('-----------------')
    bn, length = best_neighbor(st, matrix)
    print(bn, length)
