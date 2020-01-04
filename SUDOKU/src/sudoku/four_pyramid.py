from pulp import *

from sudoku import classic


class FourPyramidSudokuLP(classic.SudokuLP):

    def __init__(self, matrix):

        super().__init__(matrix)

        for k in range(1, self.n + 1):
            self += lpSum([
                lpSum([
                    self.x[r - 1][c - 1][k - 1]
                    for c in range(self.m + r, self.n - r + 1)
                ]) for r in range(1, self.m + 1)
            ]) == 1, f"in pyramid 1 only one {k + 1}"

        for k in range(1, self.n + 1):
            self += lpSum([
                lpSum([
                    self.x[r - 1][c - 1][k - 1]
                    for r in range(1 + c, self.n - self.m + 1 - c + 1)
                ]) for c in range(1, self.m + 1)
            ]) == 1, f"in pyramid 2 only one {k + 1}"

        for k in range(1, self.n + 1):
            self += lpSum([
                lpSum([
                    self.x[r - 1][c - 1][k - 1]
                    for c in range(self.n + self.m - 1 - r, r - self.m + 1)
                ]) for r in range(self.n - self.m + 1, self.n + 1)
            ]) == 1, f"in pyramid 3 only one {k + 1}"

        for k in range(1, self.n + 1):
            self += lpSum([
                lpSum([
                    self.x[r - 1][c - 1][k - 1]
                    for r in range(self.n + self.m + 1 - c, c - 1 + 1)
                ]) for c in range(self.n - self.m + 1, self.n + 1)
            ]) == 1, f"in pyramid 4 only one {k + 1}"
