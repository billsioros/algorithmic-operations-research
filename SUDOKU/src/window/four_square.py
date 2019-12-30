
import pygame
from pygame.locals import *

from window import classic
from window.detail.colors import Colors


class FourSquareSudoku(classic.Sudoku):

    def __get_corner(self, i, j, i_multiplier, j_multiplier):

        return (
            (i + i_multiplier * self.sudoku.m) * self.cell_size,
            (j + j_multiplier * self.sudoku.m) * self.cell_size
        )

    def draw(self):

        super().draw()

        for i in [1, self.sudoku.n - self.sudoku.m - 1]:
            for j in [1, self.sudoku.n - self.sudoku.m - 1]:
                for beg_multipliers in [(0, 0), (1, 1)]:
                    beg = self.__get_corner(i, j, *beg_multipliers)

                    for end_multipliers in [(0, 1), (1, 0)]:
                        end = self.__get_corner(i, j, *end_multipliers)

                        pygame.draw.line(
                            self.canvas, Colors.BLUE.value, beg, end)
