import math
import random

from utils import compute_cost
from utils import greedy_solution
from .neighbours import random_swap


def transition_probability(delta_energy, T):
    return math.exp(-delta_energy / T)


def make_transition(p):
    return random.uniform(0, 1) <= p


class SimulatedAnnealing:
    def __init__(self, init_T=None, end_T=None, cooling_factor=None):
        self.init_T = init_T if init_T else 10 * 10
        self.end_T = end_T if end_T else 0.1
        self.cooling_factor = cooling_factor if cooling_factor else 0.99
        self.final_cost = None
        self.final_path = None

    def solve(self, costs_matrix, n_iter=None, init_state=None):
        state = greedy_solution(costs_matrix) if not init_state else init_state
        current_energy = compute_cost(state, costs_matrix)
        best_state = state
        best_state_energy = current_energy
        T = self.init_T

        n_iter = 10000 if not n_iter else n_iter

        for _ in range(1, n_iter):
            candidat_state = random_swap(state)
            candidant_energy = compute_cost(candidat_state, costs_matrix)

            if(candidant_energy < current_energy):
                current_energy = candidant_energy
                state = candidat_state
                if(current_energy < best_state_energy):
                    best_state = state
                    best_state_energy = current_energy
            else:
                p = transition_probability(candidant_energy - current_energy, T)
                if make_transition(p):
                    current_energy = candidant_energy
                    state = candidat_state

            T = T * self.cooling_factor
            if T <= self.end_T:
                break

        self.final_path = best_state
        self.final_cost = best_state_energy