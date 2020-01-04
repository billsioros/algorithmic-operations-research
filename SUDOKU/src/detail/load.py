
from os import path
from re import sub
from math import sqrt


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
