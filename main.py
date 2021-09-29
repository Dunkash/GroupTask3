from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import helpers
import task_1


class Paint(object):
    DUMMY_IMAGE = "dummy.jpg"
    DUMMY_WIDTH = 600
    DUMMY_HEIGHT = 400

    def __init__(self):
        self.root = Tk()
        self.old_x = None
        self.old_y = None
        self.color = "#ff0000"

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=0)

        self.edit_mode_button = Button(self.root, text='edit mode', command=self.choose_image)
        self.edit_mode_button.grid(row=0, column=1)

        self.create_mode_button = Button(self.root, text='create mode', command=self.set_create_mode)
        self.create_mode_button.grid(row=0, column=2)
        self.active_button = self.color_button
        self.canvas = None

        self.__set_initial_view()
        self.__set_painting_mode()

    def __set_painting_mode(self):
        self.canvas.bind('<B1-Motion>', self.paint())
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def __setup(self):
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
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
        new_color = helpers.hex_to_rgb(self.color)
        self.img_arr[y][x] = new_color
        self.__sync_image()
        self.__setup()

    def fill(self, event):
        x, y = event.y, event.x
        new_color = helpers.hex_to_rgb(self.color)
        task_1.fill(x, y, new_color, self.img_arr)
        self.__sync_image()
        self.__setup()

    def set_create_mode(self):
        if self.create_mode:
            return
        self.canvas.delete('all')
        self.__set_initial_view()

    def choose_image(self):
        image_path = askopenfilename()
        if image_path != '':
            self.canvas.delete('all')
            self.create_mode = False
            self.editing_image_path = image_path
            self.__set_editing_image_view()

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button

    def paint(self, event):
        paint_color = self.color
        if self.old_x and self.old_y:
            line = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                           fill=paint_color,
                                           capstyle=ROUND, smooth=TRUE, splinesteps=36)
            print(self.canvas.coords(line))
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
