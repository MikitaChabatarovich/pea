import utils
from acs import AntColonySystem

if __name__ == "__main__":
    n = input('number of cities  ')
    m = utils.read_matrix(f'../test/{n}_test.txt')
    ant_colony = AntColonySystem()
    ant_colony.solve(m)
    prd = utils.prd(ant_colony.final_cost, utils.best_dict[int(n)])
    print(ant_colony.final_path)
    print("paths cost:", ant_colony.final_cost)
    print("PRD", prd, '%')
