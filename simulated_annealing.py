import numpy as np 
import random
import math
from time import sleep

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

def swap_random_elements(state): #better
    n = len(state)
    newstate = list(state)
    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    if i > j:
        newstate[j], newstate[i] = newstate[i], newstate[j]
    else: 
        newstate[i], newstate[j] = newstate[j], newstate[i]
    return newstate

def swap_random_neighbors(state):
    n = len(state)
    newstate = list(state)
    i = random.randint(0, n-1)
    j = i+1 if i != n-1 else -1
    if i > j:
        newstate[j], newstate[i] = newstate[i], newstate[j]
    else: 
        newstate[i], newstate[j] = newstate[j], newstate[i]
    return newstate


def transition_probability(delta_energy, T):
    return math.exp(-delta_energy/T)

def make_transition(p):
    return True if random.uniform(0,1) <= p else False 


def SimulatedAnnealing(cities, init_T, end_T, cooling_factor,init_state=None):
    n = len(cities)
    state = random_tour(n) if init_state is None else init_state
    current_energy = calc_tour_length(state, cities)
    T = init_T
    
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
               

        T  =  T*cooling_factor
        if T <= end_T:
                return state, current_energy
    return state, current_energy


if __name__ == "__main__":
    matrix = read_matrix('test/10_test.txt')
    minlength = np.Inf
    mintour = None

    init_T = 10**70
    cooling_factor = 0.99
    tour, length = SimulatedAnnealing(matrix, init_T, 0.1,  cooling_factor)
    erlist = [] 
    for _ in range(50):
        tour, length = SimulatedAnnealing(matrix, init_T, 0.1,  cooling_factor)
        error  = int((length - 212)/212*100)
        erlist.append(error)
        # print(tour, length, str(error) + "%")
    print(sum(erlist)/len(erlist))  

  
   