import numpy as np


class Node:
    def __init__(self, reduced_matrix, level, p_tour, fr, to, p_lb=None):
        self.reduced_matrix = reduced_matrix.copy()  # memory error here
        self.level = level
        self.lower_bound = self.calc_lower_bound(fr, to, p_lb)
        self.tour = p_tour.copy()
        self.city = to
        if level != 0:
            self.reduced_matrix[fr] = np.Inf
            self.reduced_matrix[:, to] = np.Inf
            self.reduced_matrix[to][0] = np.Inf
            tour = p_tour.copy()
            tour.append((fr, to))
            self.tour = tour

    @staticmethod
    def reduce_martix(matrix):
        rows_cols_min = []
        for row in matrix:
            if row.min() != np.Inf:
                rows_cols_min.append(row.min())
                row -= row.min()
        for i in range(matrix.shape[0]):
            if matrix[:, i].min() != np.Inf:
                rows_cols_min.append(matrix[:, i].min())
                matrix[:, i] -= matrix[:, i].min()
        return rows_cols_min

    def calc_lower_bound(self, fr, to, p_lb):
        cost = self.reduced_matrix[fr][to]
        rows_cols_min = Node.reduce_martix(self.reduced_matrix)
        red_cost = sum(rows_cols_min)
        if self.level == 0:
            return red_cost
        else:
            return red_cost + p_lb + cost

    def __lt__(self, other):
        a = self.lower_bound
        b = other.lower_bound
        return (a > b) ^ (a < b)
