from collections import namedtuple
import itertools

from utils import greedy_solution, compute_cost
from .neighbours import moves_map


Neighour = namedtuple('Neighour', 'path, move')


class TabuSearch:

    def __init__(self, init_state=None, n_iter=1000, tabu_size=5, move_func='swap'):
        self.n_iter = n_iter
        self.init_state = init_state
        self.tabu_size = tabu_size
        self.final_cost = None
        self.final_cost = None
        self.move_func = moves_map.get(move_func, None)
        if not self.move_func:
            raise UnknownStateGeneratorError(f'{state_gen} is uknown value for move_func. should be: {moves_map.keys()}')

    def get_neighours(self, state):
        for move in itertools.combinations(range(len(state)), 2):
            new_state = self.move_func(state, *move)
            yield Neighour(new_state, move)

    def aspiration_criteria(self, cost):
        return cost < self.final_cost

    def solve(self, matrix):
        if self.init_state is None:
            self.init_state = greedy_solution(matrix)

        current_state = self.init_state
        current_cost = compute_cost(current_state, matrix)
        best_move = None

        self.final_path = current_state
        self.final_cost = current_cost

        tabus = []

        for _ in range(self.n_iter):
            neighbours = self.get_neighours(current_state)
            neighbours_costs = map(lambda state: compute_cost(state.path, matrix), neighbours)
            neighbours_with_cost = zip(neighbours_costs, neighbours)
            for cost, neighbour in sorted(neighbours_with_cost):
                if cost < current_cost:
                    if neighbour.move not in tabus or self.aspiration_criteria(cost):
                        current_cost = cost
                        current_state = neighbour.path
                        best_move = neighbour.move

            if current_cost < self.final_cost:
                self.final_cost = current_cost
                self.final_path = current_state

            tabus.append(best_move)

            if len(tabus) > self.tabu_size:
                tabus.pop(0)
