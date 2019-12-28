
from argparse import ArgumentParser
from os import path

from misc import read_sudoku_file
from sudoku import Sudoku


if __name__ == "__main__":

    argparser = ArgumentParser(
        description='Sudoku Solver')

    argparser.add_argument(
        "-l", "--load", help="specify the file to be loaded", required=True)

    args = argparser.parse_args()

    if args.load and not path.exists(args.load):

        raise ValueError(f"'{args.load}' does not exist")

    sudoku = Sudoku(read_sudoku_file(args.load))

    sudoku.show()

    sudoku.solve()

    sudoku.show()
