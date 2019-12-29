
from argparse import ArgumentParser
from os import path
from re import fullmatch

from window import classic
from window import x


if __name__ == "__main__":

    options = {
        "sdk": classic.Window,
        "sdkx": x.Window
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

    window = options[extension](options[extension].load(args.load))

    if args.save:

        if path.exists(args.save) and not args.force:

            answer = input(f"Would you like to overwrite '{args.save}': ")

            if not fullmatch(r"y|Y|yes|YES|", answer):
                raise ValueError(
                    f"Failed to save the linear programming formulation as '{args.save}'")

        with open(args.save, "w", encoding='ascii') as file:

            print(window, file=file)

    window.loop()
