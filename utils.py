import numpy as np

def greedy_solution(matrix):
    matrix[:,0] = np.Inf
    min_index =  np.argmin(matrix[0])
    visited = [min_index]   
    while len(visited) < len(matrix) - 1:
        matrix[min_index][visited] = np.Inf
        min_index =  np.argmin(matrix[min_index])
        visited.append(min_index)
    return visited
        

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

    