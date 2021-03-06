
import sys, os

import numpy as np

import matplotlib.pyplot as plt


figure, axes = plt.subplots()

x = np.linspace(-2.5, 2.5, 500)

f1 = lambda x: x ** 3
f2 = lambda x: 3 * x ** 2

plt.plot(x, f1(x),        "-k",  label="$f_{(x)} = x^3$")
plt.plot(x, [0] * len(x), "--k")
plt.plot(x, f2(x),        ":b", label="$f^{'}_{(x)} = 3 \\cdot x^2$")

point = (0, f2(0))

axes.annotate("$f^{'}_{(0)} = 0$", xy=point, xytext=(point[0], point[1] + 0.5), ha="center")

plt.ylabel("y", color="#1C2833")
plt.xlabel("x", color="#1C2833")
plt.legend(loc="upper right")
plt.grid()
plt.xlim([-2.5, 2.5])
plt.ylim([-2.5, 2.5])

plt.show()

figure.savefig(os.path.splitext(sys.argv[0])[0] + "_figure.eps", format="eps")

