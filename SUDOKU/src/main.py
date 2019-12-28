
from sys import exit
from argparse import ArgumentParser
from os import path

import pygame
from pygame.locals import *

from enum import Enum

from sudoku import Sudoku


class Window(Sudoku):

    class Colors(Enum):

        WHITE = (255, 255, 255)
        GRAY = (127, 127, 127)
        BLACK = (0, 0, 0)

    def __init__(self, matrix, multiplier=75, title="Sudoku", font='freesansbold.ttf'):

        super().__init__(matrix)

        self.original = set([
            (i, j)
            for i in range(self.n)
            for j in range(self.n)
            if self.matrix[i][j] != 0
        ])

        pygame.init()

        self.size = self.n * multiplier
        self.cell_size = self.size // self.n

        self.font = pygame.font.Font(font, self.cell_size // 2)

        pygame.display.set_caption(f"{title} {self.n} x {self.n}")

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

        self.solve()

        def insert(value, i, j, color):

            cell_surface = self.font.render(
                '%d' % (value), True, color.value)

            cell_rectangle = cell_surface.get_rect()
            cell_rectangle.topleft = (
                i * self.cell_size +
                (self.cell_size - cell_rectangle.width) // 2,
                j * self.cell_size +
                (self.cell_size - cell_rectangle.height) // 2)

            self.canvas.blit(cell_surface, cell_rectangle)

        self.canvas.fill(Window.Colors.WHITE.value)

        for y in range(0, self.size, self.cell_size):

            pygame.draw.line(self.canvas, Window.Colors.GRAY.value,
                             (0, y), (self.size, y))

        for x in range(0, self.size, self.cell_size):

            pygame.draw.line(self.canvas, Window.Colors.GRAY.value,
                             (x, 0), (x, self.size))

        for y in range(0, self.size, self.cell_size * self.m):

            pygame.draw.line(self.canvas, Window.Colors.BLACK.value,
                             (0, y), (self.size, y))

        for x in range(0, self.size, self.cell_size * self.m):

            pygame.draw.line(self.canvas, Window.Colors.BLACK.value,
                             (x, 0), (x, self.size))

        for i in range(self.n):
            for j in range(self.n):
                insert(self.matrix[i][j], i, j,
                       Window.Colors.GRAY
                       if (i, j) not in self.original
                       else Window.Colors.BLACK)


if __name__ == "__main__":

    argparser = ArgumentParser(
        description='Sudoku Solver')

    argparser.add_argument(
        "-l", "--load", help="specify the file to be loaded", required=True)

    args = argparser.parse_args()

    if args.load and not path.exists(args.load):

        raise ValueError(f"'{args.load}' does not exist")

    matrix = Sudoku.load(args.load)

    Window(matrix).loop()
