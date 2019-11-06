
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

from os.path import splitext

from sys import argv

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


def generate_random_group(number, percentage, distance, mulitplier):

    def random_polar_coordinates(rmin, rmax):

        r = random.uniform(rmin, rmax)

        phi = random.uniform(-math.pi, +math.pi)

        return r * math.cos(phi), r * math.sin(phi)


    offset = int(percentage * number)
    number = offset if mulitplier < 0 else number - offset

    xs, ys = [], []

    for _ in range(number):

        x, y = random_polar_coordinates(distance[0], distance[1])

        xs.append(x)
        ys.append(y)

    return xs, ys


def generate_separable_group(number, percentage, distance, mulitplier, axis, line, guides):

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

    offset = int(percentage * number)
    number = offset if mulitplier < 0 else number - offset

    midpoint = (axis[0] + axis[1]) * percentage
    bounds   = (axis[0], midpoint) if mulitplier < 0 else (midpoint, axis[1])

    xs, ys = [], []

    for _ in range(number):

        x = random.uniform(bounds[0], bounds[1])
        y = f(x)

        d = mulitplier * random.uniform(distance[0], distance[1])

        xx, yy = get_dispositioned_point(line[0], (x, y), d, axis[0], axis[1])

        xs.append(xx)
        ys.append(yy)

        if guides != None and len(guides) == 3:

            plt.plot([x, xx], [y, yy], f"{guides[2]}{guides[0]}")

            plt.scatter(x, y, marker=guides[1], color=guides[0])

    return xs, ys


def generate_group(number, percentage, distance, mulitplier, axis=None, line=None, guides=None):

    if axis and line:

        return generate_separable_group(number, percentage, distance, mulitplier, axis, line, guides)

    else:

        return generate_random_group(number, percentage, distance, mulitplier)


def generate_random_points(xaxis, yaxis, number):

    xs, ys = [], []

    for _ in range(number):

        xs.append(random.uniform(xaxis[0], xaxis[1]))
        ys.append(random.uniform(yaxis[0], yaxis[1]))

    return xs, ys


if __name__ == '__main__':

    argparser = argparse.ArgumentParser(description="2D Pattern Classification via Linear Programming")

    argparser.add_argument("-g", "--guides",     help="draw guides connecting each point to the separation line",                    action="store_true")
    argparser.add_argument("-r", "--random",     help="generate the points completely at random",                                    action="store_true")
    argparser.add_argument("-f", "--figure",     help="save the figure as a '.eps' file with the given basename",                    default=None,                     type=str)
    argparser.add_argument("-s", "--seed",       help="initialize the internal state of the random number generator",                default=None,                     type=int)
    argparser.add_argument("-n", "--number",     help="specify the number of random points that make up the training set",           default=100,                      type=int)
    argparser.add_argument("-e", "--extra",      help="specify the number of random points that make up the testing set",            default=0,                        type=int)
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

        raise ValueError("'number' must be a positive integer")


    if args.extra < 0:

        raise ValueError("'extra' must be a non negative integer")


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


    if args.figure and len(args.figure) == 0:

        raise ValueError("'figure' must be a non empty string")


    if args.figure:

        figure = plt.figure()


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


        if args.extra:

            xs, ys = generate_random_points((xmin, xmax), (ymin, ymax), args.extra)

            xsa, ysa, xsb, ysb = [], [], [], []

            for i in range(len(xs)):

                if (f(xs[i]) > ys[i]) == (f(xa[0]) > 0):

                    xsa.append(xs[i])
                    ysa.append(ys[i])

                else:

                    xsb.append(xs[i])
                    ysb.append(ys[i])

            plt.scatter(xsa, ysa, marker="X", color="#ff3664", label=f"Unknown [{args.classes[0]}]")
            plt.scatter(xsb, ysb, marker="X", color="#03a1fc", label=f"Unknown [{args.classes[1]}]")

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


    if args.figure:

        figure.savefig(f"{args.figure}.eps", format="eps")

