from enum import Enum

from PIL import Image
import numpy as np
from llist import dllist, dllistnode
import queue


def fill(x, y, new_color, img_arr, line_color=None):
    new_color = np.array(new_color)
    width, height, _ = img_arr.shape
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    pixel = img_arr[x][y]
    if line_color is None:
        old_color = np.array((pixel[0], pixel[1], pixel[2]))
        flood_fill_line(old_color, new_color, img_arr, x, y)
    else:
        line_flood_fill_line(line_color, new_color, img_arr, x, y)


def fill_queue(x, y, new_color, img_arr):
    width, height, _ = img_arr.shape
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    pixel = img_arr[x][y]
    old_color = np.array((pixel[0], pixel[1], pixel[2]))
    q = queue.Queue()
    x1, y1 = x, y
    s = set()
    s.add((x1, y1))
    q.put((x1, y1))
    while not q.empty():
        x1, y1 = q.get()
        flood_fill_line_queue(old_color, new_color, img_arr, x1, y1, q, s)


def fill_with_picture(x, y, pic_arr, img_arr):
    width, height, _ = img_arr.shape
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    pixel = img_arr[x][y]
    old_color = np.array((pixel[0], pixel[1], pixel[2]))
    q = queue.Queue()
    x1, y1 = x, y
    s = set()
    s.add((x1, y1))
    q.put((x1, y1))
    while not q.empty():
        x1, y1 = q.get()
        flood_fill_with_picture(old_color, pic_arr, img_arr, x1, y1, q, s)


def flood_fill_line(old_color, new_color, img_arr, x, y):
    width, height, _ = img_arr.shape
    l, r = x, x
    if y < 0 or y >= height or x < 0 or x >= width:
        return
    for x1 in range(x, width):
        if np.array_equal(old_color, img_arr[x1][y]):
            img_arr[x1][y] = new_color
        else:
            r = x1 + 1
            break
    if r == x:
        r = width - 1
    for x1 in range(x - 1, -1, -1):
        if np.array_equal(old_color, img_arr[x1][y]):
            img_arr[x1][y] = new_color
        else:
            l = x1
            break
    if l == x:
        l = 0

    for x1 in range(l, r):
        if y + 1 < height and np.array_equal(old_color, img_arr[x1][y + 1]):
            flood_fill_line(old_color, new_color, img_arr, x1, y + 1)

    for x1 in range(l, r):
        if y - 1 >= 0 and np.array_equal(old_color, img_arr[x1][y - 1]):
            flood_fill_line(old_color, new_color, img_arr, x1, y - 1)


def line_flood_fill_line(line_color, new_color, img_arr, x, y):
    width, height, _ = img_arr.shape
    l, r = x, x
    if y < 0 or y >= height:
        return
    for x1 in range(x, width):
        if not np.array_equal(line_color, img_arr[x1][y]):
            img_arr[x1][y] = new_color
        else:
            r = x1 + 1
            break
    if r == x:
        r = width - 1
    for x1 in range(x - 1, -1, -1):
        if not np.array_equal(line_color, img_arr[x1][y]):
            img_arr[x1][y] = new_color
        else:
            l = x1
            break
    if l == x:
        l = 0
    for x1 in range(l, r):
        if y + 1 < height and not np.array_equal(line_color, img_arr[x1][y + 1]) and not np.array_equal(new_color,
                                                                                                        img_arr[x1][
                                                                                                            y + 1]):
            line_flood_fill_line(line_color, new_color, img_arr, x1, y + 1)

    for x1 in range(l, r):
        if y - 1 >= 0 and not np.array_equal(line_color, img_arr[x1][y - 1]) and not np.array_equal(new_color,
                                                                                                    img_arr[x1][
                                                                                                        y - 1]):
            line_flood_fill_line(line_color, new_color, img_arr, x1, y - 1)


class Direction(Enum):
    LEFT_UP = 0
    LEFT_DOWN = 1
    RIGHT_DOWN = 2
    RIGHT_UP = 3


def flood_fill_line_queue(old_color, new_color, img_arr, x, y, q, s):
    width, height, _ = img_arr.shape
    l, r = -1, -1
    if y < 0 or y >= height or x < 0 or x >= width:
        return
    for x1 in range(x, width):
        if np.array_equal(old_color, img_arr[x1][y]):
            img_arr[x1][y] = new_color
        else:
            r = x1
            break
    if r == -1:
        r = width - 1
    for x1 in range(x - 1, -1, -1):
        if np.array_equal(old_color, img_arr[x1][y]):
            img_arr[x1][y] = new_color
        else:
            l = x1 + 1
            break
    if l == -1:
        l = 0
    for x1 in range(l, r):
        if not (x1, y + 1) in s and y + 1 < height and np.array_equal(old_color, img_arr[x1][y + 1]):
            q.put((x1, y + 1))
            s.add((x1, y + 1))
        if not (x1, y - 1) in s and y - 1 >= 0 and np.array_equal(old_color, img_arr[x1][y - 1]):
            q.put((x1, y - 1))
            s.add((x1, y - 1))


def flood_fill_with_picture(old_color, picture_arr, img_arr, x, y, q, s):
    width, height, _ = img_arr.shape
    pic_width, pic_height, _ = picture_arr.shape
    l, r = -1, -1
    if y < 0 or y >= height or x < 0 or x >= width:
        return
    for x1 in range(x, width):
        if np.array_equal(old_color, img_arr[x1][y]):
            img_arr[x1][y] = picture_arr[x1 % pic_width][y % pic_height]
        else:
            r = x1
            break
    if r == -1:
        r = width - 1
    for x1 in range(x - 1, -1, -1):
        if np.array_equal(old_color, img_arr[x1][y]):
            img_arr[x1][y] = picture_arr[x1 % pic_width][y % pic_height]
        else:
            l = x1 + 1
            break
    if l == -1:
        l = 0

    for x1 in range(l, r):
        if not (x1, y + 1) in s and y + 1 < height and np.array_equal(old_color, img_arr[x1][y + 1]):
            q.put((x1, y + 1))
            s.add((x1, y + 1))
        if not (x1, y - 1) in s and y - 1 >= 0 and np.array_equal(old_color, img_arr[x1][y - 1]):
            q.put((x1, y - 1))
            s.add((x1, y - 1))


def colors_equals(c1, c2):
    return np.array_equal(c1, c2)


def outline(x, y, img_arr, line_color):
    l = dllist()
    x1, y1, d = get_next_point(x, y, img_arr, line_color, 0)
    if d == -1:
        return [], False
    l.append((x, y, -1))
    l.append((x1, y1, d))
    while not (x1 == x and y1 == y):
        x1, y1, d = get_next_point(x1, y1, img_arr, line_color, (d - 2) % 8)
        if d >= 0:
            l.append((x1, y1, d))
        else:
            return l, False
    return l, True


def get_next_point(x, y, img_arr, line_color, direction):
    next_coords = [
        (x, y + 1),
        (x + 1, y + 1),
        (x + 1, y),
        (x + 1, y - 1),
        (x, y - 1),
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1)
    ]
    neighbours = [img_arr[c[0]][c[1]] for c in next_coords]
    indexes = [(direction + i) % 8 for i in range(6)]
    for i in indexes:
        if colors_equals(neighbours[i], line_color):
            x1, y1 = next_coords[i]
            return x1, y1, i
    return 0, 0, -1
