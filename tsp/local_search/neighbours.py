import random


def insert(state, i, j):
    new_state = list(state)
    temp = new_state[i]
    new_state.pop(i)
    new_state.insert(j, temp)
    return new_state


def invert(state, i, j):
    new_state = list(state)
    new_state[i:j] = new_state[i:j][::-1]
    return new_state


def swap(state, i, j):
    new_state = list(state)
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state


def get_random_move(n):
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    return i, j


moves_map = {
    'insert': insert,
    'invert': invert,
    'swap': swap
}
