
import sys, os

import numpy as np

import matplotlib.pyplot as plt

from tikzplotlib import save as tikz_save


figure, axes = plt.subplots()

x = np.linspace(-2.5, 2.5, 500)

f1 = lambda x: x ** 3
f2 = lambda x: 3 * x ** 2

plt.plot(x, f1(x),        "-k",  label="$f_{(x)} = x^3$")
plt.plot(x, [0] * len(x), "-.k", label="$y = 0$")
plt.plot(x, f2(x),        "--b", label="$f^{'}_{(x)} = 3 \\cdot x^2$")

point = (0, f2(0))

axes.annotate("$f^{'}_{(x)} = 0$", xy=point, xytext=(point[0], point[1] + 1), arrowprops=dict(facecolor="black", shrink=0.1), ha="center")

plt.ylabel("y", color="#1C2833")
plt.xlabel("x", color="#1C2833")
plt.legend(loc="upper right")
plt.grid()
plt.xlim([-2.5, 2.5])
plt.ylim([-2.5, 2.5])

plt.show()

tikz_save(os.path.splitext(sys.argv[0])[0] + ".tikz", figureheight="\\figureheight", figurewidth="\\figurewidth")

