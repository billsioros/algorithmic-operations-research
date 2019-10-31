
import numpy as np

import random

import matplotlib.pyplot as plt

import argparse

from classifier import Classifier


def get_function_label(a, b):

    label="$y = {}$"

    if a == 0:

        if b == 0:

            label = label.format(f"{0:5.1f}")

        else:

            label = label.format(f"{b:5.1f}")

    else:

        if b == 0:

            label = label.format(f"{a:5.1f} \\cdot x")

        else:

            label = label.format(f"{a:5.1f} \\cdot x {b:+5.1f}")

    return label


def dispositioned_point(a, point, distance, xmin, xmax):

    x, y = point

    if a == 0.0:

        return (x, y + distance)

    a = -1.0 / a

    b = y - a * x

    v = np.subtract([xmax, a * xmax + b], [xmin, a * xmin + b])
    v = v / np.linalg.norm(v)

    return np.asarray(point) + distance * v


argparser = argparse.ArgumentParser(description="Pattern Classification via Linear Programming")

argparser.add_argument("-g", "--guides",     help="enable drawing guides connecting each point to the separation line", action="store_true")
argparser.add_argument("-x", "--xaxis",      help="specify the range of the horizontal axis",                           default=[-25.0, +25.0],           type=float, nargs='+')
argparser.add_argument("-l", "--line",       help="specify the slope and the y-intercept of the separation line",       default=[+2.0, -3.0],             type=float, nargs='+')
argparser.add_argument("-s", "--size",       help="specify the number of points to be generated",                       default=100,                      type=int)
argparser.add_argument("-p", "--percentage", help="specify the percentage of points belonging to the first class",      default=0.5,                      type=float)
argparser.add_argument("-d", "--distance",   help="specify the range of the distance from the separation line",         default=[+10.0, +80.0],           type=float, nargs='+')
argparser.add_argument("-c", "--classes",    help="specify the classes' names",                                         default=["Negative", "Positive"], type=str,   nargs='+')

args = argparser.parse_args()


if len(args.xaxis) != 2:

    tense = "was" if len(args.xaxis) == 1 else "were"

    raise Warning(f"specifying the range of the horizontal axis requires 2 values but {len(args.xaxis)} {tense} given")

if args.xaxis[0] > args.xaxis[1]:

    raise ValueError(f"the lower bound of the horizontal axis is greater than upper bound [{args.xaxis[0]:+5.2f}, {args.xaxis[1]:+5.2f}]")


if len(args.line) != 2:

    tense = "was" if len(args.xaxis) == 1 else "were"

    raise Warning(f"specifying the slope and the y-intercept of the separation line requires 2 values but {len(args.line)} {tense} given")


if args.size <= 0:

    raise ValueError("size must be a positive integer")


if args.percentage < 0.0 or args.percentage > 1.0:

    raise ValueError("percentage must be a real number in the range [0.0, 1.0]")


if len(args.distance) != 2:

    tense = "was" if len(args.distance) == 1 else "were"

    raise Warning(f"specifying the range of the distance to the separation line requires 2 values but {len(args.distance)} {tense} given")

if args.distance[0] > args.distance[1]:

    raise ValueError(f"the lower bound of the distance to the separation line is greater than upper bound [{args.distance[0]:+5.2f}, {args.distance[1]:+5.2f}]")

if args.distance[0] < 0 or args.distance[1] < 0:

    raise ValueError(f"both the lower and the upper bound of the distance to the separation line must be non negative real numbers")


if len(args.classes) != 2:

    tense = "was" if len(args.classes) == 1 else "were"

    raise Warning(f"specifying the classes' names requires 2 values but {len(args.classes)} {tense} given")


x = np.linspace(args.xaxis[0] - args.distance[1], args.xaxis[1] + args.distance[1], 500)

f = lambda x: args.line[0] * x + args.line[1]

fmin, fmax = [f(args.xaxis[0]), f(args.xaxis[1])]
fmin, fmax = min([fmin, fmax]), max([fmin, fmax])

plt.plot(x, f(x), "-k", label=get_function_label(args.line[0], args.line[1]))

midpoint = (args.xaxis[1] + args.xaxis[0]) / 2

xa, ya = [], []

for _ in range(int(args.percentage * args.size)):

    x = random.uniform(args.xaxis[0], midpoint)
    y = f(x)

    dx, dy = dispositioned_point(args.line[0], (x, y), -1.0 * random.uniform(args.distance[0], args.distance[1]), args.xaxis[0], args.xaxis[1])

    xa.append(dx)
    ya.append(dy)

    if args.guides:

        plt.plot([x, dx], [y, dy], ":r")

        plt.scatter(x, y, marker="v", color="r")


plt.scatter(xa, ya, marker="v", color="r", label=args.classes[0])

xb, yb = [], []

for _ in range(args.size - int(args.percentage * args.size)):

    x = random.uniform(midpoint, args.xaxis[1])
    y = f(x)

    dx, dy = dispositioned_point(args.line[0], (x, y), +1.0 * random.uniform(args.distance[0], args.distance[1]), args.xaxis[0], args.xaxis[1])

    xb.append(dx)
    yb.append(dy)

    if args.guides:

        plt.plot([x, dx], [y, dy], ":b")

        plt.scatter(x, y, marker="^", color="b")


plt.scatter(xb, yb, marker="^", color="b", label=args.classes[1])

classifier = Classifier([(xa[i], ya[i]) for i in range(len(xa))], [(xb[i], yb[i]) for i in range(len(xb))])

a, b = classifier.get_separator_parameters()

plt.plot(x, (lambda x: a * x + b)(x), "--k", label=get_function_label(a, b))

plt.axis('equal')
plt.xlim([args.xaxis[0], args.xaxis[1]])
plt.ylim([fmin, fmax])
plt.xlabel("$x$", color="#1C2833")
plt.ylabel("$y$", color="#1C2833")
plt.legend(loc="upper right")
plt.grid()

plt.show()

