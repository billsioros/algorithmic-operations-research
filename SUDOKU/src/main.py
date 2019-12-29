
from argparse import ArgumentParser
from os import path
from re import sub, fullmatch
from math import sqrt

from sudoku.classic import SudokuLP
from sudoku.x import SudokuXLP

from window.classic import Sudoku
from window.x import SudokuX


def load(filename):

    class ParseError(ValueError):

        def __init__(self, index, line, message):

            super().__init__(
                f"{path.basename(filename)}:{index + 1}: '{line}' {message}")

    with open(filename, 'r', encoding="ascii", errors="strict") as file:

        lines = file.readlines()
        lines = map(lambda line: sub(r"#.*", "", line), lines)
        lines = map(lambda line: sub(r"\s+", "", line), lines)
        lines = enumerate(lines)
        lines = filter(lambda data: len(data[1]) > 0, lines)

        try:
            index, line = next(lines)

            size = int(line)

            if size <= 0:
                raise ValueError

        except ValueError:
            raise ParseError(
                index, line, "is not a valid size specifier")

        _sqrt = sqrt(size)

        if _sqrt != int(_sqrt):
            raise ParseError(
                index, line, f"{size} is not a perfect square")

        matrix = [[0 for _ in range(size)] for _ in range(size)]

        for index, line in lines:
            try:
                x, y, z = tuple(map(int, line.split(',')))

                if x < 0 or y < 0 or z < 0 or z > size:
                    raise IndexError

                matrix[x - 1][y - 1] = z

            except IndexError:
                raise ParseError(
                    index, line,
                    f"is not a valid entry for a puzzle of size {size}")

            except:
                raise ParseError(
                    index, line, "Malformed entry")

    return matrix


if __name__ == "__main__":

    options = {
        "sdk": (SudokuLP, Sudoku),
        "sdkx": (SudokuXLP, SudokuX)
    }

    argparser = ArgumentParser(
        description="Creating & Solving Variations on Sudoku Puzzles")

    argparser.add_argument(
        "-l", "--load",
        help="a file representing an unsolved sudoku problem",
        required=True
    )

    argparser.add_argument(
        "-s", "--save",
        help="where to save the linear programming formulation of the given problem",
        required=False
    )

    argparser.add_argument(
        "-f", "--force",
        help="do not prompt before overwriting",
        action="store_true"
    )

    args = argparser.parse_args()

    if args.load and not path.exists(args.load):
        raise ValueError(f"'{args.load}' does not exist")

    extension = path.splitext(args.load)[1][1:]

    if extension not in options:
        raise ValueError(f"'{extension}' files are not supported")

    problem = options[extension][0](load(args.load))
    window = options[extension][1](problem)

    if args.save:

        if path.exists(args.save) and not args.force:

            answer = input(f"Would you like to overwrite '{args.save}': ")

            if not fullmatch(r"y|Y|yes|YES|", answer):
                raise ValueError(
                    f"Failed to save the linear programming formulation as '{args.save}'")

        with open(args.save, "w", encoding='ascii') as file:

            print(problem, file=file)

    window.loop()
