import random
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


class TestPaint:
    def __init__(self):
        self.root = tk.Tk()
        self.button = tk.Button(self.root, text='color', command=self.change_color)
        self.button.grid(row=0, column=0)

        # array = [[[120, 0, 80] for j in range(200)] for i in range(200)]
        im = Image.open("cat.jpeg")
        self.arr = np.array(im)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.arr))
        self.canvas = tk.Canvas(self.root, width=im.size[0], height=im.size[1])
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.grid(row=1, columnspan=5)
        self.root.mainloop()
        im.close()

    def change_color(self):
        self.arr += 20
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.arr))
        self.canvas.create_image(20, 20, anchor="nw", image=self.img)
        self.root.mainloop()

TestPaint()

# from PIL import Image
# import numpy as np
# im = Image.open("cat.jpeg")
# p = np.array(im)
# import numpy as np
#
# p = np.array((1, 2, 3))
# print(p[0])
# print(np.array_equal(p, np.array([1, 0, 3])))
# pass
