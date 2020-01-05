
from argparse import ArgumentParser
from os import path
from re import fullmatch
from math import sqrt
import numpy as np

from detail.load import load
from detail.dump import dump


def transpose(matrix):

    return list(map(list, [*zip(*matrix)]))


def relabel(matrix):

    replacements = {
        original: replacement
        for original, replacement in zip(
            range(1, len(matrix) + 1),
            np.random.permutation(range(1, len(matrix) + 1))
        )
    }

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] is not None:
                matrix[i][j] = replacements[matrix[i][j]]

    return matrix


def reorder(matrix):

    m = int(sqrt(len(matrix)))

    for p in range(m):
        for q in range(m):
            for i in range(m * p, m * (p + 1)):
                for j in range(m * q, m * (q + 1)):
                    pass

    for p in range(m):
        for q in range(m):
            for i in range(m * p, m * (p + 1)):
                for j in range(m * q, m * (q + 1)):
                    pass

    return matrix


if __name__ == "__main__":

    methods = {
        "transpose": transpose,
        "relabel": relabel,
        "reorder": reorder
    }

    argparser = ArgumentParser(
        description="Creating Variations on Sudoku Puzzles"
    )

    argparser.add_argument(
        "-l", "--load",
        help="a file representing an unsolved sudoku puzzle",
        required=True
    )

    argparser.add_argument(
        "-s", "--save",
        help="the name of the new sudoku puzzle",
        required=True
    )

    argparser.add_argument(
        "-m", "--method",
        help="the method used to create the new sudoku puzzle",
        required=True
    )

    argparser.add_argument(
        "-f", "--force",
        help="do not prompt before overwriting",
        action="store_true"
    )

    args = argparser.parse_args()

    if args.load and not path.exists(args.load):
        raise ValueError(f"'{args.load}' does not exist")

    if args.save:

        if path.exists(args.save) and not args.force:

            answer = input(f"Would you like to overwrite '{args.save}': ")

            if not fullmatch(r"y|Y|yes|YES|", answer):
                raise ValueError(
                    f"Failed to save the linear programming formulation as '{args.save}'")

    if args.method not in methods:
        raise ValueError(
            f"'{args.method}' is not a supported sudoku generation method")

    dump(methods[args.method](load(args.load)), args.save)
