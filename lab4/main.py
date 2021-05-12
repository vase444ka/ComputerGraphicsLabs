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
n_test = 7


class Node:
    def __init__(self, point, points_list, left_node = None, right_node = None):
        self.point = point
        self.points_list = points_list
        self.left_node = left_node
        self.right_node = right_node


def draw_tree(node, is_vertical_split=True, color='y'):
    if is_vertical_split:
        plt.plot([node.point[0], node.point[0]],
                 [MINY - 1, MAXY + 1],color)
    else:
        plt.plot([MINX - 1, MAXX + 1],
                 [node.point[1], node.point[1]],
                 color)
    if node.left_node != None:
        draw_tree(node.left_node, not is_vertical_split)
    if node.right_node != None:
        draw_tree(node.right_node, not is_vertical_split)


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
        generated_points.append([random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)])
    return generated_points


def generate_rectangle():
    rect = [[random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)],
            [random.uniform(MINX, MAXX), random.uniform(MINY, MAXY)]]
    if rect[0][0] > rect[1][0]:
        rect[0][0], rect[1][0] = rect[1][0], rect[0][0]
    if rect[0][1] > rect[1][1]:
        rect[0][1], rect[1][1] = rect[1][1], rect[0][1]
    return rect


def build_tree(current_points, is_vertical_split=True):
    if len(current_points) == 0:
        return None

    if is_vertical_split:
        current_points.sort(key=lambda p: p[0])
    else:
        current_points.sort(key=lambda p: p[1])
    median = len(current_points)//2

    return Node(current_points[median], current_points,
                build_tree(current_points[:median], not is_vertical_split),
                build_tree(current_points[median + 1:], not is_vertical_split))


def regional_search(rect):
    # TODO search
    result = []
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
