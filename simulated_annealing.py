import numpy as np 
import random
import math

def read_matrix(filename):
        with open(filename) as f:
           # nrows = int(f.readline())
            next(f)
            matrix = np.array(parseArr(f.readline()))
            for line in f.readlines():
                linearr = parseArr(line)
                matrix = np.vstack([matrix, linearr])
            return matrix

def parseArr(s):
        line = s.split()
        arr = [int(n) for n in line if n != '']
        return np.array(arr)      

def random_tour(n):
    return random.sample(range(1,n), n-1)      

def calc_tour_length(tour, dist_matrix):
        fr = 0
        length = 0
        for city in range(len(tour)):
            to = tour[city]
            length += dist_matrix[fr][to]
            fr = to
        length += dist_matrix[fr][0]
        return length

def swap_random_elements(state):
    n = len(state)
    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    if i > i:
        state[j], state[i] = state[i], state[j]
    else: 
        state[i], state[j] = state[j], state[i]
    return state

def swap_random_neighbors(state):
    pass


def transition_probability(delta_energy, T):
    return math.exp(-delta_energy/T)

def make_transition(p):
    return True if random.uniform(0,1) <= p else False 


def SimulatedAnnealing(cities, init_t, end_t, cooling_factor):
    n = len(cities)
    cooling_factor = 0.95
    state = random_tour(n)
    current_energy = calc_tour_length(state, cities)
    T = init_t
    
    for _ in range(1,100000):
        candidat_state = swap_random_elements(state)
        candidant_energy  = calc_tour_length(candidat_state, cities)

        if(candidant_energy < current_energy):
            current_energy = candidant_energy
            state = candidat_state
        else:
            p = transition_probability(candidant_energy - current_energy, T)
            if make_transition(p):
                current_energy = candidant_energy
                state = candidat_state

        T  -=  T*cooling_factor
        if T <= end_t:
            return state, calc_tour_length(state, cities)



if __name__ == "__main__":
    matrix = read_matrix('test/10_test.txt')

    tour, length= SimulatedAnnealing(matrix, 10**10, 0.1, 0.9)
    print(tour, length)
    tour, length= SimulatedAnnealing(matrix, 10**10, 0.1, 0.95)
    print(tour, length)
    tour, length= SimulatedAnnealing(matrix, 10**50, 0.1, 0.9)
    print(tour, length)
    tour, length= SimulatedAnnealing(matrix, 10**10, 0.1, 0.9)
    print(tour, length)