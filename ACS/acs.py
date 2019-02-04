import utils
import numpy as np
from .ant import Ant


class AntColonySystem(object):
    def __init__(self, costs_matrix, num_ants=10, num_Iter=100, alpha=0.1, beta=2, explore_probability=0.9):
        self.costs_matrix = costs_matrix
        self.size = len(costs_matrix)
        self.best_tour = None
        self.best_length = np.Inf
        self.num_ants = num_ants
        self.num_Iter = num_Iter
        self.alpha = alpha
        self.beta = beta
        self.explore_probability = explore_probability
        self.tau = 1 / \
            utils.calc_tour_length(utils.greedy_solution(
                self.costs_matrix), self.costs_matrix)
        self.pheromone_matrix = self.tau * np.ones((self.size, self.size))

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
                    1 - self.alpha) * self.pheromone_matrix[i][j] + self.alpha * self.best_tour[i][j] / self.best_length
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

    def tour_from_matrix(self):
        current = 0
        prev = 0
        tour = []
        for _ in range(self.size - 1):
            next_city = 0
            while self.best_tour[current][next_city] == 0 or prev == next_city:
                next_city += 1
            tour.append(next_city)
            prev = current
            current = next_city

        return tour

    def find_tour(self):
        for _ in range(self.num_Iter):
            lengths = np.zeros(self.num_ants)
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
                    ant.tour_length += self.costs_matrix[current][city]
                    self.local_pheromone_udpate(current, city)
            ant, best_len = self.get_min_len_and_ant(ants)
            if best_len < self.best_length:
                self.best_length = best_len
                self.best_tour = ant.path_matrix
            self.global_pheromone_udpate()
        result = self.tour_from_matrix()
        return result, utils.calc_tour_length(result, self.costs_matrix)

    def get_min_len_and_ant(self, ants):
        length = min(ant.tour_length for ant in ants)
        ant = [ant for ant in ants if ant.tour_length == length][0]
        return ant, length


if __name__ == "__main__":
    n = input('number of cities  ')
    m = utils.read_matrix(f'test/{n}_test.txt')
    ant_colony = AntColonySystem(m)
    tour, length = ant_colony.find_tour()
    print(tour)
    print("Tours length:", length)
    print("PRD", utils.prd(length, utils.best_dict[int(n)]), '%')
