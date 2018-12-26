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
        self.tau = 1 / utils.calc_tour_length(utils.greedy_solution(self.costs_matrix), self.costs_matrix)
        self.pheromone_matrix = self.tau * np.ones((self.size, self.size))
    
    def closest(self, location, visited):
        minimun = np.Inf
        result = None
        for city in range(self.size):
            if not visited[city] and self.costs_matrix[location][city] < minimun:
                minimun = self.costs_matrix[location][city]
                result = city
        return result


    def local_pheromone_udpate(self, i, j):
        self.pheromone_matrix[i][j] = (1 - self.alpha) * self.pheromone_matrix[i][j] + self.alpha*self.tau
        self.pheromone_matrix[j][i] = self.pheromone_matrix[i][j]        

    def global_pheromone_udpate(self):
        pass

    def next_city(self):
        pass

    def attraction(self):
        pass
    
    def tour_from_matrix(self):
        pass
    