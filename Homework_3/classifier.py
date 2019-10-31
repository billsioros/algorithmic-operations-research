
import numpy as np

from scipy.optimize import linprog

import matplotlib.pyplot as plt


class Classifier:

    def __init__(self, Y, Z):

        A = []

        for y in range(1, len(Y) + 1):

            A.append([0] * (y - 1) + [-1] + [0] * (len(Y) - y) + [0] * len(Z) + [-1 * Y[y - 1][0], -1 * Y[y - 1][1], +1])

        for z in range(1, len(Z) + 1):

            A.append([0] * len(Y) + [0] * (z - 1) + [-1] + [0] * (len(Z) - z) + [+1 * Z[z - 1][0], +1 * Z[z - 1][1], -1])

        for y in range(1, len(Y) + 1):

            A.append([0] * (y - 1) + [-1] + [0] * (len(Y) - y) + [0] * len(Z) + [0, 0, 0])

        for z in range(1, len(Z) + 1):

            A.append([0] * len(Y) + [0] * (z - 1) + [-1] + [0] * (len(Z) - z) + [0, 0, 0])

        A = np.asarray(A)

        b = np.asarray([-1] * (len(Y) + len(Z)) + [0] * (len(Y) + len(Z)))

        c = np.asarray([0.5] * (len(Y) + len(Z)) + [0, 0, 0])

        self.result = linprog(c, A_ub=A, b_ub=b, bounds=(None, None))


    def get_separator_parameters(self):

        a, b, c = self.result.x[-3:]

        return -1.0 * (a / b), (c / b)


if __name__ == '__main__':

    blue, red = [(0, 0), (1, 0)], [(0, 2), (1, 2)]

    classifier = Classifier(blue, red)

    for point in blue:

        plt.scatter(point[0], point[1], marker="^", color="b", label="Blue")

    for point in red:

        plt.scatter(point[0], point[1], marker="v", color="r", label="Red")

    x = np.linspace(-4, 4, 500)

    a, b = classifier.get_separator_parameters()

    plt.plot(x, (lambda x: a * x + b)(x), "--k", label="Boundary")

    plt.axis('equal')
    plt.xlim([-2, 2])
    plt.xlabel("$x$", color="#1C2833")
    plt.ylabel("$y$", color="#1C2833")
    plt.legend(loc="upper right")
    plt.grid()

    plt.show()

