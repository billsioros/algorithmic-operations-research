
import pygame
from pygame.locals import *

from window import classic
from window.detail.colors import Colors


class SudokuX(classic.Sudoku):

    def draw(self):

        super().draw()

        pygame.draw.line(self.canvas, Colors.BLUE.value,
                         (0, 0), (self.size, self.size))

        pygame.draw.line(self.canvas, Colors.BLUE.value,
                         (0, self.size), (self.size, 0))
