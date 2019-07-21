import itertools
import numpy as np
from utils import calc_tour_length


class BruteForce:
    def __init__(self):
        self.final_path = None
        self.final_cost = np.Inf

    def solve(self, costs):
        size = costs.shape[0]
        for path in itertools.permutations(range(1, size)):
            cost = compute_cost(path, costs)
            if cost < self.final_cost:
                self.final_cost = cost
                self.final_path = path
