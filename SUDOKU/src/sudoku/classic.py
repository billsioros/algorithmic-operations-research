
from pulp import *

from math import sqrt
from os import path
from re import sub


class Sudoku(LpProblem):

    @staticmethod
    def load(filename):

        class ParseError(ValueError):

            def __init__(self, index, line, message):

                super().__init__(
                    f"{path.basename(filename)}:{index + 1}: '{line}' {message}")

        with open(filename, 'r', encoding="ascii", errors="strict") as file:

            lines = file.readlines()
            lines = map(lambda line: sub(r"#.*", "", line), lines)
            lines = map(lambda line: sub(r"\s+", "", line), lines)
            lines = enumerate(lines)
            lines = filter(lambda data: len(data[1]) > 0, lines)

            try:
                index, line = next(lines)

                size = int(line)

                if size <= 0:
                    raise ValueError

            except ValueError:
                raise ParseError(
                    index, line, "is not a valid size specifier")

            _sqrt = sqrt(size)

            if _sqrt != int(_sqrt):
                raise ParseError(
                    index, line, f"{size} is not a perfect square")

            matrix = [[0 for _ in range(size)] for _ in range(size)]

            for index, line in lines:
                try:
                    x, y, z = tuple(map(int, line.split(',')))

                    if x < 0 or y < 0 or z < 0 or z > size:
                        raise IndexError

                    matrix[x - 1][y - 1] = z

                except IndexError:
                    raise ParseError(
                        index, line,
                        f"is not a valid entry for a puzzle of size {size}")

                except:
                    raise ParseError(
                        index, line, "Malformed entry")

        return matrix

    def __init__(self, matrix):

        self.matrix = matrix
        self.n = len(matrix)
        self.m = int(sqrt(self.n))

        super().__init__(
            name=f"{type(self).__name__}_{self.n}_x_{self.n}_Solver",
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

        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == 0:
                    self.matrix[i][j] = [
                        self.x[i][j][k].varValue for k in range(self.n)
                    ].index(1) + 1

        if LpStatus[self.status] != "Optimal":

            raise ValueError(
                f"Solver failed with status '{LpStatus[self.status]}'")

    def show(self):

        for line in self.matrix:

            print(' '.join([str(value) for value in line]))
