
from pulp import *

from math import sqrt


class SudokuLP(LpProblem):

    def __init__(self, matrix):

        self.matrix = matrix
        self.n = len(matrix)
        self.m = int(sqrt(self.n))

        super().__init__(
            name=f"{type(self).__name__}_solver_{self.n}_x_{self.n}".lower(),
            sense=LpMinimize)

        self.x = [
            [
                [
                    LpVariable(
                        f"x_{i + 1:02d}_{j + 1:02d}_{k + 1:02d}", cat=LpBinary)
                    for k in range(self.n)
                ] for j in range(self.n)
            ] for i in range(self.n)
        ]

        self += 0

        for j in range(self.n):
            for k in range(self.n):
                self += lpSum([self.x[i][j][k]
                               for i in range(self.n)]) == 1, f"in column {j + 1:02d} only one {k + 1:02d}"

        for i in range(self.n):
            for k in range(self.n):
                self += lpSum([self.x[i][j][k]
                               for j in range(self.n)]) == 1, f"in row {i + 1:02d} only one {k + 1:02d}"

        for k in range(self.n):
            for p in range(self.m):
                for q in range(self.m):
                    self += lpSum([
                        [
                            lpSum([
                                self.x[i][j][k]
                                for i in range(self.m * p, self.m * (p + 1))
                            ])
                        ]
                        for j in range(self.m * q, self.m * (q + 1))
                    ]) == 1, f"in submatrix {p + 1:02d} {q + 1:02d} only one {k + 1:02d}"

        for i in range(self.n):
            for j in range(self.n):
                self += lpSum([self.x[i][j][k]
                               for k in range(self.n)]) == 1, f"cell {i + 1:02d} {j + 1:02d} must be assigned exactly one value"

        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j]:
                    self += self.x[i][j][self.matrix[i][j] -
                                         1] == 1, f"cell {i + 1:02d} {j + 1:02d} has an initial value of {self.matrix[i][j]:02d}"

    def solve(self, solver=None, **kwargs):

        super().solve(solver=solver, **kwargs)

        if LpStatus[self.status] != "Optimal":

            raise ValueError(
                f"Solver failed with status '{LpStatus[self.status]}'")

        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == 0:
                    self.matrix[i][j] = [
                        self.x[i][j][k].varValue for k in range(self.n)
                    ].index(1) + 1

    def show(self):

        for line in self.matrix:

            print(' '.join([str(value) for value in line]))
