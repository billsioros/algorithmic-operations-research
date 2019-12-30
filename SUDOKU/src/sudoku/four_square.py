
from pulp import *

from sudoku import classic


class FourSquareSudokuLP(classic.SudokuLP):

    def __init__(self, matrix):

        super().__init__(matrix)

        for i in [1, self.n - self.m - 1]:
            for j in [1, self.n - self.m - 1]:
                for k in range(self.n):
                    self += lpSum([
                        [
                            lpSum([
                                self.x[r][c][k]
                                for c in range(j, j + self.m)
                            ])
                        ]
                        for r in range(i, i + self.m)
                    ]) == 1, f"in square {i + 1:02d} {j + 1:02d} {i + self.m:02d} {j + self.m:02d} only one {k + 1:02d}"
