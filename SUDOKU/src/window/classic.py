
import pygame
from pygame.locals import *

from sys import exit
from re import finditer

from window.detail.colors import Colors


class Sudoku:

    pygame.init()

    def __init__(self, sudoku, multiplier=75, debug=False):

        self.debug = debug

        self.sudoku = sudoku

        self.original = {
            (i, j)
            for i in range(self.sudoku.n)
            for j in range(self.sudoku.n)
            if self.sudoku.matrix[i][j] != 0
        }

        if not self.debug:

            self.sudoku.solve()

        self.size = self.sudoku.n * multiplier
        self.cell_size = self.size // self.sudoku.n

        self.font = pygame.font.Font('freesansbold.ttf', self.cell_size // 2)

        name = type(self).__name__

        name = ' '.join([
            match.group(0)
            for match in finditer(
                r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)",
                name)
        ])

        pygame.display.set_caption(
            f"{name} {self.sudoku.n} x {self.sudoku.n}"
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

    def highlight_cell(self, i, j, color, width=2):

        rectangle = (
            self.cell_size * j,
            self.cell_size * i,
            self.cell_size,
            self.cell_size
        )

        pygame.draw.rect(self.canvas, color.value, rectangle, width)

    def draw_cell(self, i, j, color):

        if (i, j) in self.original:
            color = Colors.GRAY

        font_surface = self.font.render(
            f"{self.sudoku.matrix[i][j]}" if self.sudoku.matrix[i][j] != 0 else '',
            True,
            color.value
        )

        font_rectangle = font_surface.get_rect()
        font_rectangle.topleft = (
            j * self.cell_size +
            (self.cell_size - font_rectangle.width) // 2,
            i * self.cell_size +
            (self.cell_size - font_rectangle.height) // 2)

        self.canvas.blit(font_surface, font_rectangle)

    def draw(self):

        self.canvas.fill(Colors.WHITE.value)

        for y in range(0, self.size, self.cell_size):

            pygame.draw.line(self.canvas, Colors.LIGHT_GRAY.value,
                             (0, y), (self.size, y))

        for x in range(0, self.size, self.cell_size):

            pygame.draw.line(self.canvas, Colors.LIGHT_GRAY.value,
                             (x, 0), (x, self.size))

        for y in range(0, self.size, self.cell_size * self.sudoku.m):

            pygame.draw.line(self.canvas, Colors.BLACK.value,
                             (0, y), (self.size, y))

        for x in range(0, self.size, self.cell_size * self.sudoku.m):

            pygame.draw.line(self.canvas, Colors.BLACK.value,
                             (x, 0), (x, self.size))

        for i in range(self.sudoku.n):
            for j in range(self.sudoku.n):
                self.draw_cell(i, j, Colors.BLACK)
