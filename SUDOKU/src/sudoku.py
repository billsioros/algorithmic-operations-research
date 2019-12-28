
from pulp import *
from math import sqrt


class Sudoku(LpProblem):

    def __init__(self, matrix):

        self.matrix = matrix
        self.n = len(matrix)
        self.m = int(sqrt(self.n))

        super().__init__(name="Sudoku", sense=LpMinimize)

        self.x = [
            [
                [
                    LpVariable(f"x_{i}_{j}_{k}", cat=LpBinary)
                    for k in range(self.n)
                ] for j in range(self.n)
            ] for i in range(self.n)
        ]

        self += 0

        for j in range(self.n):
            for k in range(self.n):
                self += lpSum([self.x[i][j][k]
                               for i in range(self.n)]) == 1, f"Only one k({k}) in column {j}"

        for i in range(self.n):
            for k in range(self.n):
                self += lpSum([self.x[i][j][k]
                               for j in range(self.n)]) == 1, f"Only one k({k}) in row {i}"

        for k in range(self.n):
            for p in range(self.m):
                for q in range(self.m):
                    self += lpSum([
                        [
                            lpSum([
                                self.x[i][j][k]
                                for i in range(self.m * p - self.m, self.m * p + 1)
                            ])
                        ]
                        for j in range(self.m * q - self.m, self.m * q + 1)
                    ]) == 1, f"Only one k({k}) in submatrix ({p},{q})"

        for i in range(self.n):
            for j in range(self.n):
                self += lpSum([self.x[i][j][k]
                               for k in range(self.n)]) == 1, f"Cell ({i},{j}) must be filled"

        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j]:
                    self += self.x[i][j][self.matrix[i][j] -
                                         1] == 1, f"Cell ({i},{j}) has an initial value of {self.matrix[i][j]}"

    def solve(self, solver=None, **kwargs):

        super().solve(solver=solver, **kwargs)

        # for i in range(self.n):
        #     for j in range(self.n):
        #         if self.matrix[i][j] == 0:
        #             self.matrix[i][j] = [
        #                 self.x[i][j][k].varValue for k in range(self.n)
        #             ].index(1) + 1

        print(LpStatus[self.status])

    def show(self):

        for line in self.matrix:

            print(' '.join([str(value) for value in line]))
