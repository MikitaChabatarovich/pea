import time
import utils

from local_search.simulated_annealing import SimulatedAnnealing
from exact_search.dynamic_programming import dp
from exact_search.brute_force import BruteForce


if __name__ == "__main__":
    n = input('number of cities  ')
    m = utils.read_matrix(f'../test/{n}_test.txt')
    solver = SimulatedAnnealing(state_gen='invert')
    start = time.monotonic()
    # solver.solve(m)
    kek = dp.solve(m, int(n))
    end = time.monotonic()
    # prd = utils.prd(solver.final_cost, utils.best_dict[int(n)])
    # print(solver.final_path)
    # print("paths cost:", solver.final_cost)
    # print("PRD", prd, '%')
    print('time elapsed', end - start)
    print(kek)
