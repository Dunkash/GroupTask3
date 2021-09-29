from PIL import Image
import numpy as np


def fill(x, y, new_color, img_arr):
    new_color = np.array(new_color)
    width, height, _ = img_arr.shape
    if x < 0 or x >= width or y < 0 or y >= height:
        return
    pixel = img_arr[x][y]
    old_color = np.array((pixel[0], pixel[1], pixel[2]))
    if np.array_equal(old_color, img_arr[x][y]):
        flood_fill_line(old_color, new_color, img_arr, x, y)


def flood_fill_line(old_color, new_color, img_arr, x, y):
    width, height, _ = img_arr.shape
    l, r = x, x
    if y < 0 or y >= height:
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
