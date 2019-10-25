
import sys, os

import numpy as np

import matplotlib.pyplot as plt

from sympy import Symbol
from sympy.solvers import solve

from scipy.optimize import linprog


x1 = np.linspace(-1, 20, 100)

f1 = lambda x1: 12.0 - 6.0 * x1
f2 = lambda x1:  7.0 - 1.5 * x1

x = Symbol("x")

y1, = solve(f1(x) - f2(x))
y2, = solve(f2(x))

figure = plt.figure()

plt.plot([0] * len(x1), x1,            "--k", label="$x_1 = 0$")
plt.plot(x1,            [0] * len(x1), "--k", label="$x_2 = 0$")

plt.plot(x1, f1(x1), "--r", label="$30 \\cdot x_1 +  5 \\cdot x_2 = 60$")
plt.plot(x1, f2(x1), "--b", label="$15 \\cdot x_1 + 10 \\cdot x_2 = 70$")

for cost in [0 + f1(0), y2 + f2(y2), y1 + f1(y1)]:

    cost_f = lambda x1: cost - x1

    plt.plot(x1, cost_f(x1), "-c", label="$x_1 + x_2 = {:05.2f}$".format(round(cost, 2)))

plt.plot([0, y2, y1], [f1(0), f2(y2), f1(y1)], "xk", markersize=10)

A = np.array([[-30, -5], [-15, -10], [0, -1], [-1, 0]])
B = np.array([-60, -70, 0, 0])
C = np.array([1, 1])

result = linprog(C, A_ub=A, b_ub=B, bounds=(0, None))

solution = (result.fun, f2(result.fun))

plt.plot(solution[0], solution[1], ".c", markersize=10)

plt.ylabel("$x_2$", color="#1C2833")
plt.xlabel("$x_1$", color="#1C2833")
plt.legend(loc="upper right")
plt.grid()
plt.xlim([-1, 8])
plt.ylim([-1, 20])

plt.show()

figure.savefig(os.path.splitext(sys.argv[0])[0] + "_figure.eps", format="eps")

