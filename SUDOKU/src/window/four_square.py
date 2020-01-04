
import pygame
from pygame.locals import *

from window import classic
from window.detail.colors import Colors


class FourSquareSudoku(classic.Sudoku):

    def draw(self):

        super().draw()

        for top_i in [1, self.sudoku.n - self.sudoku.m - 1]:
            for top_j in [1, self.sudoku.n - self.sudoku.m - 1]:
                for i in range(top_i, top_i + self.sudoku.m):
                    for j in range(top_j, top_j + self.sudoku.m):
                        self.highlight_cell(i, j, Colors.LIGHT_BLUE)
