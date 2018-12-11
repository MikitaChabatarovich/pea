import numpy as np
import random
import math
import time
from utils import read_matrix, greedy_solution, calc_tour_length


def random_tour(n):
    return random.sample(range(1, n), n - 1)


def swap_random_elements(state):  # better
    n = len(state)
    newstate = list(state)
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    if i > j:
        newstate[j], newstate[i] = newstate[i], newstate[j]
    else:
        newstate[i], newstate[j] = newstate[j], newstate[i]
    return newstate


def swap_random_neighbors(state):
    n = len(state)
    newstate = list(state)
    i = random.randint(0, n - 1)
    j = i + 1 if i != n - 1 else -1
    if i > j:
        newstate[j], newstate[i] = newstate[i], newstate[j]
    else:
        newstate[i], newstate[j] = newstate[j], newstate[i]
    return newstate

def invert(state):
    n = len(state)
    newstate = list(state)
    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    r = j - i
    if r*r == 1:
        j+=1
    if i > j:
        newstate[i:j] = newstate[i:j][::-1]
    else:
        newstate[i:j] = newstate[i:j][::-1]  
    return newstate


def transition_probability(delta_energy, T):
    return math.exp(-delta_energy / T)


def make_transition(p):
    return True if random.uniform(0, 1) <= p else False


def SimulatedAnnealing(cities, init_T, end_T, cooling_factor, init_state=None):
    n = len(cities)
    state = greedy_solution(cities) if init_state is None else init_state
    current_energy = calc_tour_length(state, cities)
    best_state = state
    best_state_energy = current_energy
    
    T = init_T
    for _ in range(1, 100000):
    
    for _ in range(1,100000000):
        candidat_state = swap_random_elements(state)
        candidant_energy = calc_tour_length(candidat_state, cities)

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
                if(current_energy < best_state_energy):
                    best_state = state
                    best_state_energy = current_energy
               
        T  =  T*cooling_factor
        if T <= end_T:
                return best_state, best_state_energy              
    return best_state, best_state_energy

def prd(value, optimal):
    return round((value - optimal)/optimal*100, 2)

if __name__ == "__main__":
    cities10 = read_matrix('test/10_test.txt')
    import time
    cooling_factor = 0.99
    end_T = 0.1
    init_T = 10*40
    minlength = np.Inf
    avg_time_list = []
    avg_prd_list = []
    for _ in range(30):
        start = time.time()
        tour, length = SimulatedAnnealing(cities=cities10, init_T=init_T, end_T=end_T, cooling_factor=cooling_factor)
        end = time.time()
        avg_time_list.append(end-start)
        avg_prd_list.append(prd(length, 212))
    avg_prd = sum(avg_prd_list)/len(avg_prd_list)
    avg_time = sum(avg_time_list)/len(avg_time_list)
    print(avg_prd, '%')
    print(avg_time)
   

