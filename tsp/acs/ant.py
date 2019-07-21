import numpy as np


class Ant:
    def __init__(self, path_size):
        self.path_size = path_size
        self.path_matrix = np.zeros((self.path_size, self.path_size), np.int8)
        self.visited = np.zeros(self.path_size, dtype=bool)
        self.current_city = None
        self.path_cost = 0
