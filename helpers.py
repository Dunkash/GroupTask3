import numpy as np


def hex_to_rgb(hex_str):
    return int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16)


class Point:

    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y


def line(x1, y1, x2, y2, img, line_color):
    beg = Point(x1, y1)
    end = Point(x2, y2)
    line_color = np.array(line_color)
    deltX = end.X - beg.X
    deltY = end.Y - beg.Y
    sX = np.sign(deltX)
    sY = np.sign(deltY)

    deltX = abs(deltX)
    deltY = abs(deltY)

    if deltX > deltY:
        pDelX, pDelY = sX, 0
        es, el = deltY, deltX
    else:
        pDelX, pDelY = 0, sY
        es, el = deltX, deltY

    err, t = round(el / 2), 0
    img[beg.X][beg.Y] = line_color

    while (t < el):
        err -= es
        if err < 0:
            err += el
            beg.X += sX
            beg.Y += sY
        else:
            beg.X += pDelX
            beg.Y += pDelY
        t += 1
        img[beg.X][beg.Y] = line_color


def lineVu(x1, y1, x2, y2, img):
    beg = Point(x1, y1)
    end = Point(x2, y2)
    if (beg.X > end.X):
        beg.X, end.X = end.X, beg.X
        beg.Y, end.Y = end.Y, beg.Y

    delX = end.X - beg.X
    delY = end.Y - beg.Y
    grad = delY / delX

    yend = beg.Y + grad * (round(beg.X) - beg.X)
    xgagp = 1 - ((beg.X + 0.5) - int(beg.X + 0.5))
    xpxl1 = round(beg.X)
    ypxl1 = int(yend)
    img.putpixel((xpxl1, ypxl1), (100, 100, 100, round(255 * (1 - (yend - int(yend))) * xgagp)))
    img.putpixel((xpxl1, ypxl1 + 1), (100, 100, 100, round(255 * (yend - int(yend)) * xgagp)))
    intery = yend + grad

    yend = end.Y + grad * (round(end.X) - end.X)
    xgap = (end.X + 0.5) - int(end.X + 0.5)
    xpxl2 = round(end.X)
    ypxl2 = int(yend)
    img.putpixel((xpxl2, ypxl2), (100, 100, 100, round(255 * (1 - (yend - int(yend))) * xgap)))
    img.putpixel((xpxl2, ypxl2 + 1), (100, 100, 100, round(255 * (yend - int(yend)) * xgap)))

    for i in range(xpxl1 + 1, xpxl2):
        img.putpixel((i, int(intery)), (100, 100, 100, round(255 * (1 - (intery - int(intery))))))
        img.putpixel((i, int(intery) + 1), (100, 100, 100, round(255 * (intery - int(intery)))))
        intery = intery + grad


def draw_line(line_cord, img_arr, line_color):
    if line_cord[0] == line_cord[2]:
        for x in range(min(line_cord[1], line_cord[3]), max(line_cord[1], line_cord[3]) + 1):
            img_arr[x, line_cord[0]] = np.array(line_color)
    else:
        for y in range(min(line_cord[0], line_cord[2]), max(line_cord[0], line_cord[2]) + 1):
            img_arr[line_cord[1], y] = np.array(line_color)


assert hex_to_rgb("#ff0000"), (255, 0, 0)
assert hex_to_rgb("#0a040b"), (10, 4, 11)
assert hex_to_rgb("#fe1000"), (254, 16, 0)
