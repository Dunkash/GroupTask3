from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import helpers
import task_1


class Paint(object):
    DUMMY_IMAGE = "dummy.png"
    SAVED_IMAGE_PATH = "saved.png"
    DUMMY_WIDTH = 600
    DUMMY_HEIGHT = 400
    LINE_COLOR = "#000000"
    CHECKING_LINE_COLOR = "#ff0000"

    def __init__(self):
        self.root = Tk()
        self.old_x = None
        self.old_y = None
        self.fill_color = "#ff0000"
        self.picture = 'picture.jpg'

        self.last_x = None
        self.last_y = None

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=0)
        self.fill_with_picture = False

        self.edit_mode_button = Button(self.root, text='edit mode', command=self.choose_image)
        self.edit_mode_button.grid(row=0, column=1)

        self.create_mode_button = Button(self.root, text='create mode', command=self.set_create_mode)
        self.create_mode_button.grid(row=0, column=2)

        self.save_button = Button(self.root, text='save', command=self.save)
        self.save_button.grid(row=0, column=3)

        self.fill_button = Button(self.root, text='fill', command=self.__set_fill_mode)
        self.fill_button.grid(row=0, column=4)

        self.fill_with_picture_button = Button(self.root, text='fill with picture',
                                               command=self.__set_fill_with_picture_mode)
        self.fill_with_picture_button.grid(row=0, column=5)

        self.circle_button = Button(self.root, text='circle', command=self.circle)
        self.circle_button.grid(row=0, column=6)

        self.active_button = self.color_button
        self.canvas = None
        self.lines_buffer = []
        self.line_rgb = helpers.hex_to_rgb(self.LINE_COLOR)

        self.__set_initial_view()

    def __set_fill_mode(self):
        self.fill_with_picture = False

    def __set_fill_with_picture_mode(self):
        self.fill_with_picture = True

    def __set_painting_mode(self):
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-2>', self.fill)

    def __setup(self):
        self.canvas.grid(row=1, columnspan=7)
        self.root.mainloop()

    def __sync_image(self):
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
        self.__set_painting_mode()
        self.__setup()

    def __set_editing_image_view(self):
        self.__set_image(self.editing_image_path)
        self.__set_painting_mode()
        self.__setup()

    def choose_color(self):
        color = askcolor(color=self.fill_color)[1]
        self.fill_color = color

    def save(self):
        save_im = Image.fromarray(self.img_arr)
        save_im.save(self.SAVED_IMAGE_PATH)

    def circle(self):
        if self.last_x != None and self.last_y != None:
            l = task_1.traverse_border(self.last_y, self.last_x, self.img_arr, self.line_rgb)
            for x, y, _ in l:
                self.img_arr[x][y] = np.array(helpers.hex_to_rgb( self.CHECKING_LINE_COLOR))
            self.__sync_image()
            self.__set_painting_mode()
            self.__setup()

    def choose_pixel(self, event):
        x, y = event.x, event.y
        rgb = self.img_arr[y][x]
        print(x, y, rgb, '\n')

    def draw_pixel(self, event):
        x, y = event.x, event.y
        new_color = helpers.hex_to_rgb(self.fill_color)
        self.img_arr[y][x] = new_color
        self.__sync_image()
        self.__setup()

    def fill(self, event):
        x, y = event.y, event.x
        if self.fill_with_picture:
            img = Image.open(self.picture)
            pic_arr = np.array(img)
            img.close()
            task_1.fill_with_picture(x, y, pic_arr, self.img_arr)
        else:
            new_color = helpers.hex_to_rgb(self.fill_color)
            task_1.fill_queue(x, y, new_color, self.img_arr)
        self.__sync_image()
        self.__set_painting_mode()
        self.__setup()

    def sync_all(self):
        self.__sync_image()
        self.save()
        self.__setup()
        # self.__set_painting_mode()
        print(1)

    def fill_until_line(self, event):
        x, y = event.y, event.x
        new_color = helpers.hex_to_rgb(self.fill_color)
        task_1.fill(x, y, new_color, self.img_arr, self.line_rgb)
        self.__sync_image()
        self.__set_painting_mode()
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
        paint_color = self.LINE_COLOR
        if self.old_x and self.old_y:
            line = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                           fill=paint_color,
                                           capstyle=ROUND, smooth=TRUE, splinesteps=36)
            line_coord = self.canvas.coords(line)
            print(line_coord)
            lb = self.lines_buffer
            # if (len(lb) != 0):
            #     last = lb[len(lb) - 1]
            #     lb.append([last[2], last[3], line_coord[0], line_coord[1]])
            lb.append([int(x) for x in line_coord])
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = self.old_x, self.old_y
        self.old_x, self.old_y = None, None
        for line in self.lines_buffer:
            helpers.line(line[1], line[0], line[3], line[2], self.img_arr, self.line_rgb)
        self.__sync_image()
        self.__set_painting_mode()
        self.__setup()
        self.lines_buffer.clear()


p = None


def sync():
    p.sync_all()


if __name__ == '__main__':
    p = Paint()
