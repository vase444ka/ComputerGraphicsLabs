import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from matplotlib.collections import LineCollection
import random

from sympy.vector import Vector

MINX = 0.
MAXX = 10.
MINY = 0.
MAXY = 10.

# number of slabs
k = 10

# total number of points
n = 50


def generate_points(n):
    points = []
    for i in range(n):
        points.append([random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)])
    return points


def distance_to_segment(point, segment):
    return Segment(*segment).distance(Point(point)).evalf()


def is_left_turn(start, end, point):
    x_1 = end[0] - start[0]
    y_1 = end[1] - start[1]
    x_2 = point[0] - start[0]
    y_2 = point[1] - start[1]
    if x_1*y_2 - x_2*y_1 > 0:
        return True
    else:
        return False


def rec_fh(current_points, segment):
    if len(current_points) == 0:
        return []
    farmost_point = max(current_points,
                        key=lambda cur: distance_to_segment(cur, segment))
    left_points = []
    right_points = []
    for point in points:
        if point != farmost_point:
            if is_left_turn(segment[0], farmost_point, point):
                left_points.append(point)
            if is_left_turn(farmost_point, segment[1], point):
                right_points.append(point)

    return rec_fh(left_points, (segment[0], farmost_point)) + \
           [farmost_point] + \
           rec_fh(right_points, (farmost_point, segment[1]))


def fast_hull(points):#TODO order in return
    leftmost = min(points)
    rightmost = max(points)
    left_points = []
    right_points = []
    for point in points:
        if point != leftmost and point != rightmost:
            if is_left_turn(leftmost, rightmost, point):
                left_points.append(point)
            if is_left_turn(rightmost, leftmost, point):
                right_points.append(point)

    print(leftmost)
    print(rightmost)
    print(left_points)
    print(right_points)

    return [leftmost] + rec_fh(left_points, (leftmost, rightmost)) + \
           [rightmost] + rec_fh(right_points, (rightmost, leftmost))


def draw(points=[], hull=[]):
    fig, ax = plt.subplots()
    ax.set_xlim([MINX - 1, MAXX + 1])
    ax.set_ylim([MINY - 1, MAXY + 1])

    plt.plot(list(map(lambda x: x[0], points)), list(map(lambda x: x[1], points)), 'r.')
    print(hull)
    plt.plot(list(map(lambda x: x[0], hull)), list(map(lambda x: x[1], hull)), 'bo')

    lines = [[hull[-1], hull[0]]]
    lc = LineCollection(lines, linewidths=1)
    ax.add_collection(lc)

    plt.show()


if __name__ == '__main__':
    points = generate_points(n)
    hull = fast_hull(points)
    draw(points, hull)
