
def dump(matrix, filename):

    with open(filename, 'w', encoding="ascii") as file:

        file.write(f"{len(matrix)}\n")

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix is not None:
                    file.write(f"{i + 1}, {j + 1}, {matrix[i][j]}")
