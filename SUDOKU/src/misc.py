
import os
import re
import math


def read_sudoku_file(filename, expected_extension="sdk"):

    extension = os.path.splitext(filename)[1]

    if extension[1:] != expected_extension:
        raise ValueError(f"'{extension}' files are not supported")

    with open(filename, 'r', encoding="ascii", errors="strict") as file:

        lines = [
            re.sub(r"\s+", "", line) for line in file.readlines()
        ]

        try:
            size = int(lines[0])
        except:
            raise ValueError(f"'{lines[0]}' is not a valid size specifier")

        sqrt = math.sqrt(size)

        if sqrt != math.floor(sqrt):
            raise ValueError(f"{size} is not a perfect square")

        matrix = [[0 for _ in range(size)] for _ in range(size)]

        for i in range(1, len(lines)):
            try:
                x, y, z = tuple(
                    map(lambda value: int(value) - 1, lines[i].split(',')))

                matrix[x][y] = z
            except IndexError:
                raise ValueError(
                    f"'{lines[i]}' is not a valid entry for a puzzle of size {size}")
            except:
                raise ValueError(f"Malformed entry '{lines[i]}'")

    return matrix
