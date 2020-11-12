# Standard libraries
from tkinter import *
from tkinter import ttk
import csv
import datetime

# Imported libraries
from PIL import Image, ImageTk


class iSpindelTabGUI(Frame):
    """A class for 'iSpindel' tab creation"""

    def __init__(self, tab_control, ispindel_parameters):
        super().__init__(tab_control)
        self.name = 'iSpindel'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('None', '14'))
        self.ispindel_parameters = ispindel_parameters
        self.w_scale = 0.0
        self.h_scale = 0.0

        # Images for labels
        self.img_ispindel = Image.open('images/ispindel2.bmp')
        self.img_ispindel_copy = self.img_ispindel.copy()
        self.img_c_ispindel = ImageTk.PhotoImage(image=self.img_ispindel)

        # Names of GUI objects in the tab
        self.c_ispindel = Canvas(self)

        # CATIA coordinates
        self.ispindel_rect = (400, 225)
        filename = 'data/ispindel_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.ispindel_coords = {}

            for row in reader:
                self.ispindel_coords[row[0]] = (int(row[1]), int(row[2]))

        # Adding images to GUI objects
        self.c_background = self.c_ispindel.create_image(0, 0, anchor=N + W, image=self.img_c_ispindel)

        self.c_items = {}
        self.c_dots = {}
        self.c_lines = {}

        # Adding GUI objects to the grid
        self.c_ispindel.place(relwidth=1, relheight=1)

        # Adding commands to GUI objects
        self.c_ispindel.bind('<Configure>', self.resize_image)

        # TEST
        self.c_ispindel.bind('<Button-1>', self.draw_indicators)

    def resize_image(self, event):
        width, height = event.width, event.height

        self.w_scale = width / self.img_ispindel.width
        self.h_scale = height / self.img_ispindel.height

        # Resizing images
        # img_ispindel
        image = self.img_ispindel_copy.resize((width, height))
        self.img_c_ispindel = ImageTk.PhotoImage(image)
        self.c_ispindel.itemconfig(self.c_background, image=self.img_c_ispindel)

        # Coordinates of GUI objects
        if self.c_dots and self.c_lines:
            for key, value in self.ispindel_coords.items():
                self.c_ispindel.coords(
                    self.c_lines[key],
                    int(round(self.w_scale * self.img_ispindel.width * (value[0] / self.ispindel_rect[0]), 0)),
                    int(round(self.h_scale * self.img_ispindel.height * (value[1] / self.ispindel_rect[1]), 0)),
                    1000,
                    1000)
                self.c_ispindel.coords(
                    self.c_dots[key],
                    int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0]) - 10), 0)),
                    int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1]) - 10), 0)),
                    int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0]) + 10), 0)),
                    int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1]) + 10), 0)))

    # def button_switch(self, key=None):
    #     self.brewery_parameters.verify_parameters(key)
    #
    #     for key, value in self.brewery_parameters.parameters.items():
    #         if self.brewery_parameters.parameters[key]:
    #             self.c_brewery.itemconfig(self.c_items[key], image=self.img_c_button_on)
    #         else:
    #             self.c_brewery.itemconfig(self.c_items[key], image=self.img_c_button_off)

    def draw_indicators(self, event):
        # Draw dots
        for key, value in self.ispindel_coords.items():
            self.c_dots[key] = self.c_ispindel.create_oval(
                int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0]) - 10), 0)),
                int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1]) - 10), 0)),
                int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0]) + 10), 0)),
                int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1]) + 10), 0)),
                fill='black')

        # Draw lines in realtime
        difference = 0.5
        start = datetime.datetime.now()
        stop = start + datetime.timedelta(seconds=difference)

        while (stop - datetime.datetime.now()).total_seconds() >= 0:
            for key, value in self.ispindel_coords.items():
                xa = int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0])), 0))
                ya = int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1])), 0))
                xb = 1000
                yb = 1000
                a = (ya - yb) / (xa - xb)
                b = ya - a * xa
                x = xa + (xb - xa) * (1 - (stop - datetime.datetime.now()).total_seconds() / difference)
                y = a * x + b

                self.c_ispindel.delete(key)

                self.c_lines[key] = self.c_ispindel.create_line(
                    int(round(self.w_scale * self.img_ispindel.width * (value[0] / self.ispindel_rect[0]), 0)),
                    int(round(self.h_scale * self.img_ispindel.height * (value[1] / self.ispindel_rect[1]), 0)),
                    x, y, width=2, tags=key)

            self.c_ispindel.update_idletasks()
