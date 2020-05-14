import numpy as np

import utils
from .ant import Ant


class AntColonySystem(object):
    def __init__(self, num_ants=10, num_iter=100, alpha=0.1, beta=2, explore_probability=0.9):
        self.costs_matrix = None
        self.size = None
        self.best_path = None
        self.best_cost = np.Inf
        self.num_ants = num_ants
        self.num_iter = num_iter
        self.alpha = alpha
        self.beta = beta
        self.explore_probability = explore_probability

    def compute_tau(self, costs_matrix):
        return 1.0 / utils.compute_cost(utils.greedy_solution(
            self.costs_matrix), self.costs_matrix)

    def closest(self, ant):
        minimun = np.Inf
        result = None
        for city in range(self.size):
            if not ant.visited[city] and self.costs_matrix[ant.current_city][city] < minimun:
                minimun = self.costs_matrix[ant.current_city][city]
                result = city
        return result

    def local_pheromone_udpate(self, i, j):
        self.pheromone_matrix[i][j] = (
            1 - self.alpha) * self.pheromone_matrix[i][j] + self.alpha * self.tau
        self.pheromone_matrix[j][i] = self.pheromone_matrix[i][j]

    def global_pheromone_udpate(self):
        for i in range(self.size):
            for j in range(i + 1, self.size):
                self.pheromone_matrix[i][j] = (
                    1 - self.alpha) * self.pheromone_matrix[i][j] + self.alpha * self.best_path[i][j] / self.best_cost
                self.pheromone_matrix[j][i] = self.pheromone_matrix[i][j]

    def next_city(self, ant):
        result_city = None
        q = np.random.random_sample()
        if q <= self.explore_probability:
            maximum = - np.Inf
            for city in range(self.size):
                if not ant.visited[city]:
                    f = self.attraction(ant.current_city, city)
                    if f > maximum:
                        maximum = f
                        result_city = city
            if maximum != 0:
                return result_city
            else:
                result_city = self.closest(ant)
                return result_city
        else:
            prob_sum = 0
            for city in range(self.size):
                if not ant.visited[city]:
                    prob_sum += self.attraction(ant.current_city, city)
            if prob_sum == 0:
                result_city = self.closest(ant)
                return result_city
            else:
                R = np.random.random_sample()
                s = 0
                for city in range(self.size):
                    if not ant.visited[city]:
                        s += self.attraction(ant.current_city, city) / prob_sum
                        if s > R:
                            return city

    def attraction(self, i, j):
        if i + j and i != j:
            result = self.pheromone_matrix[i][j] / \
                np.power(self.costs_matrix[i][j], self.beta)
            return result
        else:
            return 0

    def path_from_matrix(self):
        current = 0
        prev = 0
        path = []
        for _ in range(self.size - 1):
            next_city = 0
            while self.best_path[current][next_city] == 0 or prev == next_city:
                next_city += 1
            path.append(next_city)
            prev = current
            current = next_city

        return path

    def solve(self, costs_matrix):
        self.costs_matrix = costs_matrix
        self.size = len(costs_matrix)
        self.tau = self.compute_tau(self.costs_matrix)
        self.pheromone_matrix = self.tau * np.ones((self.size, self.size))
        for _ in range(self.num_iter):
            ants = [Ant(self.size) for _ in range(self.num_ants)]
            for ant in ants:
                ant.visited[0] = True
                ant.current_city = 0
            for step in range(self.size):
                for ant in ants:
                    current = ant.current_city
                    if step < self.size - 1:
                        city = self.next_city(ant)
                    else:
                        city = 0
                    ant.current_city = city
                    ant.visited[city] = True
                    ant.path_matrix[current][city] = 1
                    ant.path_matrix[city][current] = 1
                    ant.path_cost += self.costs_matrix[current][city]
                    self.local_pheromone_udpate(current, city)
            ant, best_len = self.get_min_len_and_ant(ants)
            if best_len < self.best_cost:
                self.best_cost = best_len
                self.best_path = ant.path_matrix
            self.global_pheromone_udpate()
        self.final_path = self.path_from_matrix()
        self.final_cost = utils.compute_cost(self.final_path, self.costs_matrix)

    def get_min_len_and_ant(self, ants):
        cost = min(ant.path_cost for ant in ants)
        ant = [ant for ant in ants if ant.path_cost == cost][0]
        return ant, cost
