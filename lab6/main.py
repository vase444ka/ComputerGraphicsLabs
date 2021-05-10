import math

import matplotlib.pyplot as plt
from celluloid import Camera
import random

MINX = 0.
MAXX = 10.
MINY = 0.
MAXY = 10.

# total number of points
n = 50

# number of points for jarvis method
min_n = 3


def draw():
    ax.set_xlim([MINX - 1, MAXX + 1])
    ax.set_ylim([MINY - 1, MAXY + 1])
    plt.plot(list(map(lambda x: x[0], points)), list(map(lambda x: x[1], points)), 'bo')


def draw_step(first, second):
    draw()
    first.append(first[0])
    plt.plot(list(map(lambda x: x[0], first)), list(map(lambda x: x[1], first)), 'yo-')

    second.append(second[0])
    plt.plot(list(map(lambda x: x[0], second)), list(map(lambda x: x[1], second)), 'yo-')

    camera.snap()


def define_hull(current_hull):
    draw()
    current_hull.append(current_hull[0])
    plt.plot(list(map(lambda x: x[0], current_hull)), list(map(lambda x: x[1], current_hull)), 'ro-')
    camera.snap()


def generate_points():
    generated_points = []
    for i in range(n):
        generated_points.append([random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)])
    return generated_points


def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def cross_product(start, end, point):
    x_1 = end[0] - start[0]
    y_1 = end[1] - start[1]
    x_2 = point[0] - start[0]
    y_2 = point[1] - start[1]
    return x_1 * y_2 - x_2 * y_1


def dot_product(start, end, point):
    x_1 = end[0] - start[0]
    y_1 = end[1] - start[1]
    x_2 = point[0] - start[0]
    y_2 = point[1] - start[1]
    return x_1 * x_2 + y_1 * y_2


def is_left_turn(start, end, point):
    if cross_product(start, end, point) >= 0:
        return True
    else:
        return False


def angle(start, end, point):
    return dot_product(start, end, point) / (dist(start, end) * dist(start, point))


def jarvis_march(current_points):
    return current_points#TODO


def graham_unite(current_points):
    start = min(current_points)
    current_points.remove(start)
    current_points = sorted(current_points,
                            key=lambda point: -angle(start, (start[0], start[1] + 1), point))

    stack = [start, current_points[0]]
    for i in range(1, len(current_points)):
        while not is_left_turn(stack[-1], stack[-2], current_points[i]):
            del stack[-1]
        stack.append(current_points[i])
    return stack


def find_hull(point_set):
    first_set = point_set[:len(point_set) // 2]
    second_set = point_set[len(point_set) // 2:]

    first_set = (jarvis_march(first_set) if len(first_set) <= min_n else find_hull(first_set))
    second_set = (jarvis_march(second_set) if len(second_set) <= min_n else find_hull(second_set))
    resulting_hull = graham_unite(first_set + second_set)

    draw_step(first_set[:], second_set[:])
    define_hull(resulting_hull[:])
    return resulting_hull


if __name__ == '__main__':
    # initialization
    points = generate_points()
    fig, ax = plt.subplots()
    camera = Camera(fig)

    hull = find_hull(points)

    # final animation
    anim = camera.animate(repeat=False, interval=1000)
    plt.show()
