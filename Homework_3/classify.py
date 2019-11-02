
# MIT License
#
# Copyright (c) 2019 Vasileios Sioros
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np

import math

import random

import matplotlib.pyplot as plt

import argparse

from classifier2d import Classifier2D


def get_line_label(a, b):

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


def generate_random_group(size, percentage, distance, mulitplier):

    def random_polar_coordinates(rmin, rmax):

        r = random.uniform(rmin, rmax)

        phi = random.uniform(-math.pi, +math.pi)

        return r * math.cos(phi), r * math.sin(phi)


    size = int(percentage * size) if mulitplier < 0 else size - int(percentage * size)

    xs, ys = [], []

    for _ in range(size):

        x, y = random_polar_coordinates(distance[0], distance[1])

        xs.append(x)
        ys.append(y)

    return xs, ys


def generate_separable_group(size, percentage, distance, mulitplier, axis, line, guides):

    def get_dispositioned_point(a, point, distance, xmin, xmax):

        x, y = point

        if a == 0.0:

            return (x, y + distance)

        a = -1.0 / a

        b = y - a * x

        v = np.subtract([xmax, a * xmax + b], [xmin, a * xmin + b])
        v = v / np.linalg.norm(v)

        return np.asarray(point) + distance * v


    f = lambda x: line[0] * x + line[1]

    size = int(percentage * size) if mulitplier < 0 else size - int(percentage * size)

    midpoint = (axis[0] + axis[1]) * percentage

    bounds = (axis[0], midpoint) if mulitplier < 0 else (midpoint, axis[1])

    xs, ys = [], []

    for _ in range(size):

        x = random.uniform(bounds[0], bounds[1])
        y = f(x)

        xx, yy = get_dispositioned_point(line[0], (x, y), mulitplier * random.uniform(distance[0], distance[1]), axis[0], axis[1])

        xs.append(xx)
        ys.append(yy)

        if guides != None and len(guides) == 3:

            plt.plot([x, xx], [y, yy], f"{guides[2]}{guides[0]}")

            plt.scatter(x, y, marker=guides[1], color=guides[0])

    return xs, ys


def generate_group(size, percentage, distance, mulitplier, axis=None, line=None, guides=None):

    if axis and line:

        return generate_separable_group(size, percentage, distance, mulitplier, axis, line, guides)

    else:

        return generate_random_group(size, percentage, distance, mulitplier)


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description="2D Pattern Classification via Linear Programming")

    argparser.add_argument("-g", "--guides",     help="draw guides connecting each point to the separation line",                    action="store_true")
    argparser.add_argument("-r", "--random",     help="generate the points completely at random",                                    action="store_true")
    argparser.add_argument("-s", "--seed",       help="initialize the internal state of the random number generator",                default=None,                     type=int)
    argparser.add_argument("-n", "--number",     help="specify the number of points to be generated",                                default=100,                      type=int)
    argparser.add_argument("-p", "--percentage", help="specify the percentage of points belonging to the first class",               default=0.5,                      type=float)
    argparser.add_argument("-x", "--axis",       help="specify the lower and upper bounds of the horizontal axis",                   default=[-25.0, +25.0],           type=float, nargs='+')
    argparser.add_argument("-l", "--line",       help="specify the slope and the y-intercept of the separation line",                default=[+2.0, -3.0],             type=float, nargs='+')
    argparser.add_argument("-d", "--distance",   help="specify the lower and upper bounds of the distance from the separation line", default=[+10.0, +80.0],           type=float, nargs='+')
    argparser.add_argument("-c", "--classes",    help="specify the classes' labels",                                                 default=["Negative", "Positive"], type=str,   nargs='+')

    args = argparser.parse_args()


    if len(args.axis) != 2:

        tense = "was" if len(args.axis) == 1 else "were"

        raise Warning(f"specifying the range of the horizontal axis requires 2 values but {len(args.axis)} {tense} given")

    if args.axis[0] > args.axis[1]:

        raise ValueError(f"the lower bound of the horizontal axis is greater than upper bound [{args.axis[0]:+5.2f}, {args.axis[1]:+5.2f}]")


    if len(args.line) != 2:

        tense = "was" if len(args.axis) == 1 else "were"

        raise Warning(f"specifying the slope and the y-intercept of the separation line requires 2 values but {len(args.line)} {tense} given")


    if args.number <= 0:

        raise ValueError("'size' must be a positive integer")


    if args.percentage <= 0.0 or args.percentage >= 1.0:

        raise ValueError("'percentage' must be a real number in the range (0.0, 1.0)")


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


    if args.seed:

        random.seed(args.seed)


    x = np.linspace(args.axis[0] - args.distance[1], args.axis[1] + args.distance[1], 500)

    f = lambda x: args.line[0] * x + args.line[1]

    if not args.random and args.guides:

        plt.plot(x, f(x), ":k", label=get_line_label(args.line[0], args.line[1]))


    if args.random:

        xa, ya = generate_group(args.number, args.percentage, args.distance, -1)
        xb, yb = generate_group(args.number, args.percentage, args.distance, +1)

    else:

        xa, ya = generate_group(args.number, args.percentage, args.distance, -1, args.axis, args.line, ("r", "v", ":") if args.guides else None)
        xb, yb = generate_group(args.number, args.percentage, args.distance, +1, args.axis, args.line, ("b", "^", ":") if args.guides else None)

    xmin, xmax = min(xa + xb), max(xa + xb)
    ymin, ymax = min(ya + yb), max(ya + yb)

    plt.scatter(xa, ya, marker="v", color="r", label=args.classes[0])
    plt.scatter(xb, yb, marker="^", color="b", label=args.classes[1])


    try:

        group_1 = [(xa[i], ya[i]) for i in range(len(xa))]
        group_2 = [(xb[i], yb[i]) for i in range(len(xb))]

        classifier = Classifier2D(group_1, group_2)

        a, b = classifier.get_separator_parameters()

        f = lambda x: a * x + b

        plt.plot(x, f(x), "-k", label=get_line_label(a, b))

    except:

        pass

    plt.axis('equal')
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.xlabel("$x$", color="#1C2833")
    plt.ylabel("$y$", color="#1C2833")
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

