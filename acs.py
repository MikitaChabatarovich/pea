import utils
import numpy as np


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

    def closest(self, location, visited):
        minimun = np.Inf
        result = None
        for city in range(self.size):
            if not visited[city] and self.costs_matrix[location][city] < minimun:
                minimun = self.costs_matrix[location][city]
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

    def next_city(self, ant, location, visited):
        result_city = None
        q = np.random.random_sample()
        if q <= self.explore_probability:
            maximum = - np.Inf
            for city in range(self.size):
                if not visited[city]:
                    f = self.attraction(location, city)
                    if f > maximum:
                        maximum = f
                        result_city = city
            if maximum != 0:
                return result_city
            else:
                result_city = self.closest(location, visited)
                return result_city
        else:
            prob_sum = 0
            for city in range(self.size):
                if not visited[city]:
                    prob_sum += self.attraction(location, city)
            if prob_sum == 0:
                result_city = self.closest(location, visited)
                return result_city
            else:
                R = np.random.random_sample()
                s = 0
                for city in range(self.size):
                    if not visited[city]:
                        s += self.attraction(location, city) / prob_sum
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
        location = np.zeros(self.num_ants, np.int32)

        for _ in range(self.num_Iter):
            visited = np.zeros((self.num_ants, self.size), dtype=bool)
            tours = [np.zeros((self.size, self.size), np.int8)
                     for ant in range(self.num_ants)]
            lengths = np.zeros(self.num_ants)
            for ant in range(self.num_ants):
                visited[ant][0] = True
            for step in range(self.size):
                for ant in range(self.num_ants):
                    current = location[ant]
                    if step < self.size - 1:
                        city = self.next_city(ant, location[ant], visited[ant])
                    else:
                        city = 0
                    location[ant] = city
                    visited[ant][city] = True
                    tours[ant][current][city] = 1
                    tours[ant][city][current] = 1
                    lengths[ant] += self.costs_matrix[current][city]
                    self.local_pheromone_udpate(current, city)
            best_len = min(lengths)
            if best_len < self.best_length:
                self.best_length = best_len
                self.best_tour = tours[np.argmin(lengths)]
            self.global_pheromone_udpate()
        result = self.tour_from_matrix()
        return result, utils.calc_tour_length(result, self.costs_matrix)


if __name__ == "__main__":
    n = input('number of cities  ')
    m = utils.read_matrix(f'test/{n}_test.txt')
    ant_colony = AntColonySystem(m)
    tour, length = ant_colony.find_tour()
    print(tour)
    print("Tours length:", length)
    print("PRD", utils.prd(length, utils.best_dict[int(n)]), '%')
