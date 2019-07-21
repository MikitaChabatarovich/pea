import utils
import ACS
import time
from tsp.brute_force import BruteForce

if __name__ == '__main__':
    n = input('number of cities  ')
    m = utils.read_matrix(f'test/{n}_test.txt')
    # ant_colony = ACS.AntColonySystem(m)
    # start = time.time()
    # tour, length = ant_colony.find_tour()
    # end = time.time()
    # print("Tour:", tour)
    # print("Tours length:", length)
    # print("PRD", utils.prd(length, utils.best_dict[int(n)]), '%')
    # print("Time elapsed:", round(end - start, 2))
    bf = BruteForce()
    bf.solve(m)
    print('path: ', bf.final_path)
    print('cost: ', bf.final_cost)
