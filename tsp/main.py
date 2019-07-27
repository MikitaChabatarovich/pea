import time
import utils
# from acs import AntColonySystem
# from bnb import BranchAndBound
from local_search.simulated_annealing import SimulatedAnnealing

if __name__ == "__main__":
    n = input('number of cities  ')
    m = utils.read_matrix(f'../test/{n}_test.txt')
    solver = SimulatedAnnealing()
    start = time.monotonic()
    solver.solve(m)
    end = time.monotonic()
    prd = utils.prd(solver.final_cost, utils.best_dict[int(n)])
    print(solver.final_path)
    print("paths cost:", solver.final_cost)
    print("PRD", prd, '%')
    print('time elapsed', end - start)
