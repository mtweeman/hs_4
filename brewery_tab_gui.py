# Standard libraries
from tkinter import *
import csv

# Imported libraries
from PIL import Image, ImageTk

# My libraries


class BreweryTabGUI(Frame):
    """A class for Brewery tab creation"""
    def __init__(self, tab_control, brewery_parameters):
        super().__init__(tab_control)
        self.name = 'Brewery'
        self.brewery_parameters = brewery_parameters
        self.w_scale = 1.0
        self.h_scale = 1.0

        # Images for labels
        self.img_brewery = Image.open('images/test7.bmp')
        self.img_button_on = Image.open('images/button_on.png')
        self.img_button_off = Image.open('images/button_off.png')

        self.img_brewery_copy = self.img_brewery.copy()
        self.img_button_on_copy = self.img_button_on.copy()
        self.img_button_off_copy = self.img_button_off.copy()

        self.img_c_brewery = ImageTk.PhotoImage(image=self.img_brewery)
        self.img_c_button_on = ImageTk.PhotoImage(image=self.img_button_on)
        self.img_c_button_off = ImageTk.PhotoImage(image=self.img_button_off)

        # CATIA coordinates for GUI objects
        filename = 'data/brewery_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.brewery_coords = {}

            for row in reader:
                if row[0] == 'rect':
                    self.brewery_rect = (int(row[1]), int(row[2]))
                else:
                    self.brewery_coords[row[0]] = (int(row[1]), int(row[2]))

        # Names of GUI objects in the tab
        self.c_brewery = Canvas(self)

        # c_brewery
        self.c_items = {}
        self.c_background = self.c_brewery.create_image(0, 0, anchor=N + W, image=self.img_c_brewery)

        for k, v in self.brewery_coords.items():
            self.c_items[k] = self.c_brewery.create_image(
                int(round(self.w_scale * self.img_brewery.width * (v[0] / self.brewery_rect[0]), 0)),
                int(round(self.h_scale * self.img_brewery.height * (v[1] / self.brewery_rect[1]), 0)),
                anchor=CENTER, image=self.img_c_button_off)

        # Adding GUI objects to the grid
        self.c_brewery.place(relwidth=1, relheight=1)

        # Adding commands to GUI objects
        self.c_brewery.bind('<Configure>', self.resize_image)

        for k, v in self.brewery_coords.items():
            self.c_brewery.tag_bind(self.c_items[k], '<Button-1>', lambda event, key=k: self.button_switch(key))

    def resize_image(self, event):
        # Getting scale
        width, height = event.width, event.height

        self.w_scale = width / self.img_brewery.width
        self.h_scale = height / self.img_brewery.height

        # Resizing images
        # img_brewery
        image = self.img_brewery_copy.resize((width, height))
        self.img_c_brewery = ImageTk.PhotoImage(image)

        # img_button_on
        image = self.img_button_on_copy.resize((int(round(self.w_scale * self.img_button_on.width, 0)),
                                                int(round(self.h_scale * self.img_button_on.height, 0))))
        self.img_c_button_on = ImageTk.PhotoImage(image)

        # img_button_off
        image = self.img_button_off_copy.resize((int(round(self.w_scale * self.img_button_off.width, 0)),
                                                 int(round(self.h_scale * self.img_button_off.height, 0))))
        self.img_c_button_off = ImageTk.PhotoImage(image)

        # Updating canvas
        self.c_brewery.itemconfig(self.c_background, image=self.img_c_brewery)
        self.update_buttons()

        # Updating coordinates of GUI objects
        for k, v in self.brewery_coords.items():
            self.c_brewery.coords(self.c_items[k],
                                  int(round(self.w_scale * self.img_brewery.width * (v[0] / self.brewery_rect[0]), 0)),
                                  int(round(self.h_scale * self.img_brewery.height * (v[1] / self.brewery_rect[1]), 0)))

    def button_switch(self, key):
        self.brewery_parameters.verify_parameters(key)
        self.update_buttons()

    def update_buttons(self):
        for k in self.c_items:
            if self.brewery_parameters.parameters[k]:
                self.c_brewery.itemconfig(self.c_items[k], image=self.img_c_button_on)
            else:
                self.c_brewery.itemconfig(self.c_items[k], image=self.img_c_button_off)
