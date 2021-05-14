import math

import matplotlib.pyplot as plt
from celluloid import Camera
import random
from matplotlib import patches

MINX = 0.
MAXX = 10.
MINY = 0.
MAXY = 10.

# total number of points
n = 15

# number of points for jarvis method
n_test = 15


class Node:
    def __init__(self, point, points_list, minx, maxx, miny, maxy, left_node=None, right_node=None):
        self.point = point
        self.miny = miny
        self.maxy = maxy
        self.minx = minx
        self.maxx = maxx
        self.points_list = points_list
        self.left_node = left_node
        self.right_node = right_node


def draw_tree(node, is_vertical_split=True, color=(1., 0., 0.)):
    if is_vertical_split:
        plt.plot([node.point[0], node.point[0]],
                 [node.miny, node.maxy], color=color)
    else:
        plt.plot([node.minx, node.maxx],
                 [node.point[1], node.point[1]], color=color)

    increment = 1/(round(math.log2(n)) + 3)
    new_color = (color[0] - increment, 0., color[2] + increment)
    if node.left_node is not None:
        draw_tree(node.left_node, not is_vertical_split, new_color)
    if node.right_node is not None:
        draw_tree(node.right_node, not is_vertical_split, new_color)


def draw():
    ax.set_xlim([MINX - 1, MAXX + 1])
    ax.set_ylim([MINY - 1, MAXY + 1])
    draw_tree(root)
    plt.plot(list(map(lambda x: x[0], points)), list(map(lambda x: x[1], points)), 'bo')


def draw_step(located_points, rectangle):
    draw()
    ax.add_patch(patches.Rectangle((rectangle[0][0], rectangle[0][1]),
                                   rectangle[1][0] - rectangle[0][0], rectangle[1][1] - rectangle[0][1],
                                   linewidth=1, edgecolor='g', facecolor='none'))
    plt.plot(list(map(lambda x: x[0], located_points)), list(map(lambda x: x[1], located_points)), 'r.')
    camera.snap()


def generate_points():
    generated_points = []
    for i in range(n):
        generated_points.append([(random.uniform(MINX, MAXX)), (random.uniform(MINY, MAXY))])
    return generated_points


def generate_rectangle():
    rect = [[random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)],
            [random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)]]
    if rect[0][0] > rect[1][0]:
        rect[0][0], rect[1][0] = rect[1][0], rect[0][0]
    if rect[0][1] > rect[1][1]:
        rect[0][1], rect[1][1] = rect[1][1], rect[0][1]
    return rect


def build_tree(current_points, is_vertical_split=True, minx=MINX - 1, maxx=MAXX + 1, miny=MINY - 1, maxy=MAXY + 1):
    if len(current_points) == 0:
        return None
    # TODO copypaste
    if is_vertical_split:
        current_points.sort(key=lambda p: p[0])
        median = len(current_points) // 2
        midx = current_points[median][0]
        return Node(current_points[median], current_points,
                    minx, maxx, miny, maxy,
                    build_tree(current_points[:median], not is_vertical_split, minx, midx, miny, maxy),
                    build_tree(current_points[median + 1:], not is_vertical_split, midx, maxx, miny, maxy))
    else:
        current_points.sort(key=lambda p: p[1])
        median = len(current_points) // 2
        midy = current_points[median][1]
        return Node(current_points[median], current_points,
                    minx, maxx, miny, maxy,
                    build_tree(current_points[:median], not is_vertical_split, minx, maxx, miny, midy),
                    build_tree(current_points[median + 1:], not is_vertical_split, minx, maxx, midy, maxy))


def rec_search(rect, node):
    result = []

    if rect[0][0] <= node.point[0] <= rect[1][0] and \
            rect[0][1] <= node.point[1] <= rect[1][1]:
        result += [node.point]
    if rect[0][0] > rect[1][0] or rect[0][1] > rect[1][1]:
        return []
    if rect[0][0] == node.minx and rect[0][1] == node.miny and \
            rect[1][0] == node.maxx and rect[1][1] == node.maxy:
        return node.current_points

    if node.left_node is not None:
        new_rect = [rect[0], (min(rect[1][0], node.left_node.maxx), min(rect[1][1], node.left_node.maxy))]
        result += rec_search(new_rect, node.left_node)
    if node.right_node is not None:
        new_rect = [(max(rect[0][0], node.left_node.minx), max(rect[0][1], node.left_node.miny)), rect[1]]
        result += rec_search(new_rect, node.right_node)
    return result


def regional_search(rect):
    result = rec_search(rect, root)
    draw_step(result, rect)


if __name__ == '__main__':
    # initialization
    points = generate_points()
    fig, ax = plt.subplots()
    camera = Camera(fig)

    root = build_tree(points)
    for i in range(0, n_test):
        regional_search(generate_rectangle())

    # final animation
    anim = camera.animate(repeat=False, interval=1000)
    plt.show()
