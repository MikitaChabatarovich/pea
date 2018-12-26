import utils
import numpy as np

class AntColonySystem:
    def __init__(self, costs_matrix, num_ants=10,num_Iter=100,alpha=0.1,beta=2,explore_probability=0.9):
        self.costs_matrix = costs_matrix
        self.size = len(costs_matrix)
        self.best_tour = None
        self.best_length = np.Inf 
        self.num_ants = num_ants
        self.num_Iter = num_Iter
        self.alpha = alpha
        self.beta = beta
        self.explore_probability = explore_probability
        # self.tau = ??
        # self.pheromone = ??