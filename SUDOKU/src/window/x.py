
import pygame
from pygame.locals import *

from window import classic
from window.detail.colors import Colors


class SudokuX(classic.Sudoku):

    def draw(self):

        super().draw()

        for i in range(self.sudoku.n):
            self.highlight_cell(i, i, Colors.LIGHT_BLUE)

        for i in range(self.sudoku.n):
            self.highlight_cell(self.sudoku.n - 1 - i, i, Colors.LIGHT_BLUE)
