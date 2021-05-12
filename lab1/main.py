import math

import matplotlib.pyplot as plt
from celluloid import Camera
import random
from sympy import *
import numpy as np

MINX = 0.
MAXX = 10.
MINY = 0.
MAXY = 10.

# total number of polygon vertices
n = 56


def draw(intersections):
    ax.set_xlim([MINX - 1, MAXX + 1])
    ax.set_ylim([MINY - 1, MAXY + 1])
    polygon.append(polygon[0])
    plt.plot(list(map(lambda x: x[0], polygon)), list(map(lambda x: x[1], polygon)), 'b-')

    line_segment = [tuple(line.intersection(Line(Point(0, 0), Point(0, 1)))[0].evalf()),
                    tuple(line.intersection(Line(Point(MAXX, 0), Point(MAXX, 1)))[0].evalf())]

    plt.plot(list(map(lambda x: x[0], line_segment)), list(map(lambda x: x[1], line_segment)), 'y-')

    plt.plot(point[0], point[1], "ro")

    intersect_points = list(map(lambda x: x[0], intersections))
    plt.plot(list(map(lambda x: x[0], intersect_points)), list(map(lambda x: x[1], intersect_points)), 'yo')
    camera.snap()


def has_polygon_vertex(line):
    for point in polygon:
        if line.distance(point) == 0:
            return True
    return False


def generate_point():
    return Point(random.uniform(MINX, MAXX), random.uniform(MINY, MAXY))


def read_polygon():
    generated_points = []
    with open('input.txt', 'r') as reader:
        n = int(reader.readline())
        for i in range(n):
            coords = list(map(int, reader.readline().split(' ')))
            generated_points.append((coords[0], coords[1]))

    return generated_points


def generate_line():
    x, y = 0., point.y
    step = 0.01
    line = Line(point, Point(x, y))
    while has_polygon_vertex(line):
        y += step
        line = Line(point, Point(x, y))
    return line


def is_point_in_polygon():
    intersections = []
    for i in range(0, len(polygon)):
        polygon_side = Segment(polygon[i], polygon[(i + 1) % len(polygon)])
        crossing_point = line.intersection(Line(polygon[i], polygon[(i + 1) % len(polygon)]))
        if len(crossing_point) == 1 and \
                polygon_side.distance(crossing_point[0]) == 0 and \
                crossing_point[0].x < point.x:
            intersections.append(crossing_point)

        draw(intersections)

    if (len(intersections) % 2 == 1):
        return True
    else:
        return False


if __name__ == '__main__':
    # initialization
    polygon = read_polygon()#read points from file
    #polygon = [Point(0, 1), Point(0, 3), Point(3, 3), Point(3, 6), Point(0, 6), Point(0, 9), Point(6, 9), Point(6, 0)]
    point = generate_point()
    line = generate_line()
    fig, ax = plt.subplots()
    camera = Camera(fig)

    if is_point_in_polygon():
        plt.text(MINX, MAXY//2, "IN POLYGON")
    else:
        plt.text(MINX, MAXY//2, "NOT IN POLYGON")
    camera.snap();

    # final animation
    anim = camera.animate(repeat=False, interval=2000)
    plt.show()
