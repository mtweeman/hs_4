# Standard libraries
from tkinter import *
from tkinter import ttk
import csv

# Imported libraries
from PIL import Image, ImageTk


class FermentationTabGUI(Frame):
    """A class for 'Fermentation' tab creation"""

    def __init__(self, tab_control, fermentation_parameters):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('None', '14'))
        self.fermentation_parameters = fermentation_parameters

        # Images for labels
        self.img_fermentation = Image.open('images/ferm4.bmp')
        self.img_switch_on = Image.open('images/switch_on.png')
        self.img_switch_off = Image.open('images/switch_off.png')
        self.img_button_on = Image.open('images/button_on.png')
        self.img_button_off = Image.open('images/button_off.png')

        self.img_switch_on = self.img_switch_on.resize((60, 38))
        self.img_switch_off = self.img_switch_off.resize((60, 38))
        self.img_button_on = self.img_button_on.resize((32, 32))
        self.img_button_off = self.img_button_off.resize((32, 32))

        self.img_fermentation_copy = self.img_fermentation.copy()
        self.img_switch_on_copy = self.img_switch_on.copy()
        self.img_switch_off_copy = self.img_switch_off.copy()
        self.img_button_on_copy = self.img_button_on.copy()
        self.img_button_off_copy = self.img_button_off.copy()

        self.img_c_fermentation = ImageTk.PhotoImage(image=self.img_fermentation)
        self.img_c_switch_on = ImageTk.PhotoImage(image=self.img_switch_on)
        self.img_c_switch_off = ImageTk.PhotoImage(image=self.img_switch_off)
        self.img_c_button_on = ImageTk.PhotoImage(image=self.img_button_on)
        self.img_c_button_off = ImageTk.PhotoImage(image=self.img_button_off)

        # Names of GUI objects in the tab
        self.c_fermentation = Canvas(self)

        self.c_items = {}
        self.c_vessels = {}

        # CATIA coordinates
        self.fermentation_rect = (1776, 999)
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.fermentation_coords = {}

            for row in reader:
                self.fermentation_coords[row[0]] = (int(row[1]), int(row[2]))

        # Adding images to GUI objects
        self.c_background = self.c_fermentation.create_image(0, 0, anchor=N + W, image=self.img_c_fermentation)

        for key, value in self.fermentation_coords.items():
            if 'fv' in key:
                self.c_items[key] = self.c_fermentation.create_image(
                    int(round(self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.img_fermentation.height * (value[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_switch_off,
                    tags=key)
                self.c_vessels[key] = self.c_fermentation.create_text(
                    int(round(self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.img_fermentation.height * (value[1] / self.fermentation_rect[1]) + 40, 0)),
                    anchor=CENTER, font=(None, 14), text=key.replace('_', ' ').upper())
            else:
                self.c_items[key] = self.c_fermentation.create_image(
                    int(round(self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.img_fermentation.height * (value[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_button_off,
                    tags=key)

        # Adding GUI objects to the grid
        self.c_fermentation.place(relwidth=1, relheight=1)

        # Adding commands to GUI objects
        self.c_fermentation.bind('<Configure>', self.resize_image)

        for key, value in self.fermentation_coords.items():
            self.c_fermentation.tag_bind(self.c_items[key], '<Button-1>', lambda event, key=key: self.toggle_switch(key))

    def resize_image(self, event):
        width, height = event.width, event.height

        w_scale = width / self.img_fermentation.width
        h_scale = height / self.img_fermentation.height

        # Resizing images
        # img_brewery
        image = self.img_fermentation_copy.resize((width, height))
        self.img_c_fermentation = ImageTk.PhotoImage(image)
        self.c_fermentation.itemconfig(self.c_background, image=self.img_c_fermentation)

        # img_switch_on
        image = self.img_switch_on_copy.resize(
            (int(round(w_scale * self.img_switch_on.width, 0)), int(round(h_scale * self.img_switch_on.height, 0))))
        self.img_c_switch_on = ImageTk.PhotoImage(image)

        # img_switch_off
        image = self.img_switch_off_copy.resize(
            (int(round(w_scale * self.img_switch_off.width, 0)), int(round(h_scale * self.img_switch_off.height, 0))))
        self.img_c_switch_off = ImageTk.PhotoImage(image)

        # img_button_on
        image = self.img_button_on_copy.resize(
            (int(round(w_scale * self.img_button_on.width, 0)), int(round(h_scale * self.img_button_on.height, 0))))
        self.img_c_button_on = ImageTk.PhotoImage(image)

        # img_button_off
        image = self.img_button_off_copy.resize(
            (int(round(w_scale * self.img_button_off.width, 0)), int(round(h_scale * self.img_button_off.height, 0))))
        self.img_c_button_off = ImageTk.PhotoImage(image)

        self.toggle_switch()

        # Coordinates of GUI objects
        for key, value in self.fermentation_coords.items():
            self.c_fermentation.coords(self.c_items[key],
                                  int(round(w_scale * self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                                  int(round(h_scale * self.img_fermentation.height * (value[1] / self.fermentation_rect[1]), 0)))
            if 'fv' in key:
                self.c_fermentation.coords(self.c_vessels[key],
                                           int(round(w_scale * self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                                           int(round(h_scale * (self.img_fermentation.height * (value[1] / self.fermentation_rect[1]) + 40), 0)))

    def toggle_switch(self, key=None):
        self.fermentation_parameters.verify_parameters(key)

        for key, value in self.fermentation_parameters.parameters.items():
            if 'fv' in key:
                if self.fermentation_parameters.parameters[key]:
                    self.c_fermentation.itemconfig(self.c_items[key], image=self.img_c_switch_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[key], image=self.img_c_switch_off)
            else:
                if self.fermentation_parameters.parameters[key]:
                    self.c_fermentation.itemconfig(self.c_items[key], image=self.img_c_button_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[key], image=self.img_c_button_off)
