
import pygame
from pygame.locals import *

from sys import exit

from window.detail.colors import Colors


class Sudoku:

    pygame.init()

    def __init__(self, sudoku, multiplier=75):

        self.sudoku = sudoku

        self.original = {
            (i, j)
            for i in range(self.sudoku.n)
            for j in range(self.sudoku.n)
            if self.sudoku.matrix[i][j] != 0
        }

        self.sudoku.solve()

        self.size = self.sudoku.n * multiplier
        self.cell_size = self.size // self.sudoku.n

        self.font = pygame.font.Font('freesansbold.ttf', self.cell_size // 2)

        pygame.display.set_caption(
            f"{type(self).__name__} {self.sudoku.n} x {self.sudoku.n}"
        )

        self.canvas = pygame.display.set_mode((self.size, self.size))

    def loop(self):

        while True:

            self.draw()

            for event in pygame.event.get():

                if event.type == QUIT:

                    pygame.quit()
                    exit()

            pygame.display.update()

    def draw(self):

        def draw_cell(i, j):

            if (i, j) in self.original:
                color = Colors.GRAY
            else:
                color = Colors.BLACK

            cell_surface = self.font.render(
                '%d' % (self.sudoku.matrix[i][j]),
                True,
                color.value
            )

            cell_rectangle = cell_surface.get_rect()
            cell_rectangle.topleft = (
                j * self.cell_size +
                (self.cell_size - cell_rectangle.width) // 2,
                i * self.cell_size +
                (self.cell_size - cell_rectangle.height) // 2)

            self.canvas.blit(cell_surface, cell_rectangle)

        self.canvas.fill(Colors.WHITE.value)

        for y in range(0, self.size, self.cell_size):

            pygame.draw.line(self.canvas, Colors.GRAY.value,
                             (0, y), (self.size, y))

        for x in range(0, self.size, self.cell_size):

            pygame.draw.line(self.canvas, Colors.GRAY.value,
                             (x, 0), (x, self.size))

        for y in range(0, self.size, self.cell_size * self.sudoku.m):

            pygame.draw.line(self.canvas, Colors.BLACK.value,
                             (0, y), (self.size, y))

        for x in range(0, self.size, self.cell_size * self.sudoku.m):

            pygame.draw.line(self.canvas, Colors.BLACK.value,
                             (x, 0), (x, self.size))

        for i in range(self.sudoku.n):
            for j in range(self.sudoku.n):
                draw_cell(i, j)
