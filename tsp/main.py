from collections import namedtuple
import time

import pprint

import utils

from local_search.simulated_annealing import SimulatedAnnealing
from local_search.tabu_search import TabuSearch
from exact_search.dynamic_programming import Dynamic
from exact_search.branch_and_bound import BranchAndBound
from exact_search.brute_force import BruteForce
from population_search.acs import AntColonySystem

solvers = [
    SimulatedAnnealing(state_gen='invert'),
    TabuSearch(),
    Dynamic(),
    BruteForce(),
    AntColonySystem(),
    BranchAndBound(),
]


def get_test_matrix(n_cities):
    return utils.read_matrix(f'../test/{n_cities}_test.txt')


Score = namedtuple('Score', 'name, time, path, cost, prd')


def evaluate_solver(solver, matrix, n):
    start = time.monotonic()
    solver.solve(matrix)
    end = time.monotonic()
    score = Score(
        name=solver.__class__.__name__,
        time=end - start,
        path=solver.final_path,
        cost=solver.final_cost,
        prd=utils.prd(solver.final_cost, utils.best_dict[int(n)])
    )
    return score


if __name__ == "__main__":
    n = input('number of cities  ')
    matrix = get_test_matrix(n)
    scores = [evaluate_solver(solver, matrix, int(n)) for solver in solvers]
    pprint.pprint(scores)
