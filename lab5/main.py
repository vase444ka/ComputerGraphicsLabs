import time

import matplotlib.pyplot as plt
from celluloid import Camera
from sympy import *
from matplotlib.collections import LineCollection
import random

MINX = 0.
MAXX = 10.
MINY = 0.
MAXY = 10.

# total number of points
n = 50

def draw():
    ax.set_xlim([MINX - 1, MAXX + 1])
    ax.set_ylim([MINY - 1, MAXY + 1])
    plt.scatter(list(map(lambda x: x[0], points)), list(map(lambda x: x[1], points)), c=colors)


def draw_step(segment, farmost_point):
    draw()
    plt.plot(list(map(lambda x: x[0], segment)), list(map(lambda x: x[1], segment)), 'go-')
    plt.plot(farmost_point[0], farmost_point[1], 'go-')
    camera.snap()


def define_hull(hull):
    draw()
    hull.append(hull[0])
    plt.plot(list(map(lambda x: x[0], hull)), list(map(lambda x: x[1], hull)), 'bo-')
    camera.snap()

def generate_points():
    generated_points = []
    for i in range(n):
        generated_points.append([random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)])
    return generated_points


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
    colors[points.index(farmost_point)] = "b"

    draw_step(segment, farmost_point)
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


def fast_hull(points):
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


    return [leftmost] + rec_fh(left_points, (leftmost, rightmost)) + \
           [rightmost] + rec_fh(right_points, (rightmost, leftmost))


if __name__ == '__main__':
    points = generate_points()#random generation
    colors = ["r"] * len(points)#points are red. Hull points are blue.
    fig, ax = plt.subplots()
    camera = Camera(fig)

    hull = fast_hull(points)

    define_hull(hull)#draws final hull

    anim = camera.animate(repeat=False, interval=3000)
    plt.show()