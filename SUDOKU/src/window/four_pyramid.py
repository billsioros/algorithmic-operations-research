
import pygame
from pygame.locals import *

from window import classic
from window.detail.colors import Colors


class FourPyramidSudoku(classic.Sudoku):

    def draw(self):

        super().draw()

        for i in range(1, self.sudoku.m + 1):
            for j in range(self.sudoku.m + i, self.sudoku.n - i + 1):
                self.highlight_cell(i - 1, j - 1, Colors.LIGHT_BLUE)

        for j in range(1, self.sudoku.m + 1):
            for i in range(1 + j, self.sudoku.n - self.sudoku.m + 1 - j + 1):
                self.highlight_cell(i - 1, j - 1, Colors.LIGHT_BLUE)

        for i in range(self.sudoku.n - self.sudoku.m + 1, self.sudoku.n + 1):
            for j in range(self.sudoku.n + self.sudoku.m - 1 - i, i - self.sudoku.m + 1):
                self.highlight_cell(i - 1, j - 1, Colors.LIGHT_BLUE)

        for j in range(self.sudoku.n - self.sudoku.m + 1, self.sudoku.n + 1):
            for i in range(self.sudoku.n + self.sudoku.m + 1 - j, j - 1 + 1):
                self.highlight_cell(i - 1, j - 1, Colors.LIGHT_BLUE)
