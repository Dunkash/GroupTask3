from colour import Color
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import numpy as np


class Point:
    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y


def hex_to_rgb(hex_str):
    return int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16)


class Paint(object):
    DUMMY_IMAGE = "dummy.jpg"
    DUMMY_WIDTH = 600
    DUMMY_HEIGHT = 400

    def __init__(self):
        self.root = Tk()
        self.old_x = 0
        self.old_y = 0
        self.color = "#ff0000"
        self.img = None
        self.points = []
        self.count = 0

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=0)
        self.active_button = self.color_button
        self.canvas = None

        self.__set_initial_view()
        self.__set_painting_mode()

    def __set_painting_mode(self):
        self.canvas.bind('<Button-1>', self.paint())

    def __setup(self):
        self.canvas.bind('<Button-1>', self.paint)
        self.canvas.grid(row=1, columnspan=5)
        self.root.mainloop()

    def __sync_image(self):
        if self.canvas is None:
            self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.img_tk = ImageTk.PhotoImage(image=Image.fromarray(self.img_arr))
        self.canvas.create_image(0, 0, anchor='nw', image=self.img_tk)

    def __set_image(self, img_path):
        img = Image.open(img_path)
        self.width, self.height = img.size
        self.img_arr = np.array(img)
        self.__sync_image()
        img.close()

    def __set_initial_view(self):
        self.create_mode = True
        self.has_changes = False
        self.editing_image_path = None
        self.width = self.DUMMY_WIDTH
        self.height = self.DUMMY_HEIGHT
        self.__set_image(self.DUMMY_IMAGE)
        self.__setup()

    def __set_editing_image_view(self):
        self.__set_image(self.editing_image_path)
        self.__setup()

    def choose_color(self):
        color = askcolor(color=self.color)[1]
        self.color = color

    def choose_pixel(self, event):
        x, y = event.x, event.y
        rgb = self.img_arr[y][x]
        print(x, y, rgb, '\n')

    def draw_pixel(self, event):
        x, y = event.x, event.y
        new_color = hex_to_rgb(self.color)
        self.img_arr[y][x] = new_color
        self.__sync_image()
        self.__setup()

    def fillTriagle(self, p1, p2, p3):
        if p1.y > p2.y:
            p1, p2 = p2, p1
        if p1.y > p3.y:
            p1, p3 = p3, p1
        if p2.y > p3.y:
            p2, p3 = p3, p2
        height = p3.y - p1.y
        i = p1.y
        colors = ()
        for i in range(p1.y, p2.y):
            segment_height = p2.y - p1.y + 1
            alpha = float((i - p1.y) / height)
            beta = float((i - p1.y) / segment_height)
            newX = int(p1.x + (p3.x - p1.x) * alpha)
            newY = int(p1.y + (p3.y - p1.y) * alpha)
            a = Point(newX, newY, p1.color)
            newX = int(p1.x + (p2.x - p1.x) * beta)
            newY = int(p1.y + (p2.y - p1.y) * beta)
            b = Point(newX, newY, p2.color)
            if a.x > b.x:
                a, b = b, a
            j = a.x
            if (b.x - a.x) > 0:
                color = Color(p1.color)
                colors = list(color.range_to(Color(p2.color), b.x - a.x))
                index = 0
                for j in range(a.x, b.x):
                    self.canvas.create_rectangle(j, i, j, i, outline=colors[index].hex)
                    index += 1
        i = p2.y
        for i in range(p2.y, p3.y):
            segment_height = p3.y - p2.y + 1
            alpha = float((i - p1.y) / height)
            beta = float((i - p2.y) / segment_height)
            newX = int(p1.x + (p3.x - p1.x) * alpha)
            newY = int(p1.y + (p3.y - p1.y) * alpha)
            a = Point(newX, newY, p1.color)
            newX = int(p2.x + (p3.x - p2.x) * beta)
            newY = int(p2.y + (p3.y - p2.y) * beta)
            b = Point(newX, newY, p2.color)
            if a.x > b.x:
                a, b = b, a
            j = a.x
            if (b.x - a.x) > 0:
                #color = Color(colors[0].web)
                color = Color(p2.color)
                colors = list(color.range_to(Color(p3.color), b.x - a.x))
                index = 0
                for j in range(a.x, b.x):
                    self.canvas.create_rectangle(j, i, j, i, outline=colors[index].hex)
                    index += 1

    def paint(self, event):
        paint_color = self.color
        self.points.append(Point(event.x, event.y, paint_color))
        self.canvas.create_rectangle(event.x, event.y+1, event.x, event.y + 1 , outline=paint_color, width=0.2)
        self.old_x = event.x
        self.old_y = event.y
        self.count += 1
        print(self.count)
        if self.count == 3:
            self.fillTriagle(self.points[0], self.points[1], self.points[2])
            self.count = 0
            self.points = []

    def reset(self, event):
        self.old_x, self.old_y = 0, 0


if __name__ == '__main__':
    Paint()
