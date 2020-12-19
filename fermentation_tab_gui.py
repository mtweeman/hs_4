# Standard libraries
from tkinter import *
from tkinter import ttk
import csv

# Imported libraries
from PIL import Image, ImageTk

# My libraries
from sparkline_gui import SparklinesGUI

class FermentationTabGUI(Frame):
    """A class for 'Fermentation' tab creation"""

    def __init__(self, tab_control, fermentation_parameters, database, dpi):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.fermentation_parameters = fermentation_parameters
        self.database = database
        self.dpi = dpi

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
        self.f_frames = {}
        self.l_labels = {}
        self.f_sparklines = {}

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
            if 'fv' in key or 'master' in key:
                self.c_items[key] = self.c_fermentation.create_image(
                    int(round(self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.img_fermentation.height * (value[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_switch_off,
                    tags=key)

                if 'fv' in key:
                    self.f_frames[key] = Frame(self)
                    self.l_labels[key] = Label(self.f_frames[key], fg='white', bg='#555555', font=(None, 14), text=key.replace('_', ' ').upper())
                    self.f_sparklines[key] = SparklinesGUI(self.f_frames[key], self.database, self.dpi)
            else:
                self.c_items[key] = self.c_fermentation.create_image(
                    int(round(self.img_fermentation.width * (value[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.img_fermentation.height * (value[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_button_off,
                    tags=key)

        # Adding GUI objects to the grid
        self.c_fermentation.place(relwidth=1, relheight=1)

        for key, value in self.fermentation_coords.items():
            if 'fv' in key:
                self.f_frames[key].place(relx=value[0] / self.fermentation_rect[0],
                                         rely=(value[1] + self.img_switch_on.height) / self.fermentation_rect[1],
                                         relwidth=0.1,
                                         relheight=0.2,
                                         anchor=N)
                self.l_labels[key].grid(row=0, column=0, sticky=NSEW)
                self.f_sparklines[key].grid(row=1, column=0, sticky=NSEW)
                batch_number = self.database.get_fermentation_settings_batch_number(key)
                if batch_number:
                    self.f_sparklines[key].update_sparklines(batch_number)

        # Setting rows and columns properties
        for k in self.f_frames:
            self.f_frames[k].columnconfigure(0, weight=1)
            self.f_frames[k].rowconfigure(1, weight=1)

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

    def toggle_switch(self, key=None):
        if key:
            self.fermentation_parameters.verify_parameters(key)

        # Update images
        for k in self.fermentation_parameters.parameters:
            if 'fv' in k or 'master' in k:
                if self.fermentation_parameters.parameters[k]:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_switch_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_switch_off)
            else:
                if self.fermentation_parameters.parameters[k]:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_button_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_button_off)

        self.c_fermentation.update_idletasks()

        if key:
            # Update database
            if 'fv' in key:
                self.database.execute_fermentation_settings_log(key, self.fermentation_parameters.parameters[key])
            elif 'master' in key:
                if self.fermentation_parameters.parameters[key]:
                    ispindel_name = self.database.get_fermentation_settings_ispindel_name(key.replace('master', 'fv'))
                    self.database.execute_ispindel_settings_master(ispindel_name)
                else:
                    self.database.execute_ispindel_settings_master()

            # Update data on screen
            if 'fv' in key:
                if (not self.fermentation_parameters.parameters[key] and
                    not self.fermentation_parameters.parameters[key.replace('fv', 'master')]):
                    self.l_labels[key].config(text=key.replace('_', ' ').upper())
            elif 'master' in key:
                if (not self.fermentation_parameters.parameters[key] and
                    not self.fermentation_parameters.parameters[key.replace('master', 'fv')]):
                    self.l_labels[key.replace('master', 'fv')].config(text=key.replace('master_', 'fv ').upper())

    def update_parameters(self, socket_message):
        # Check for data logging by fermentation_vessel OR master for freezer
        result = self.database.get_fermentation_settings(socket_message['name'], True)
        if not result:
            result = self.database.get_fermentation_settings(socket_message['name'], False)

        if result:
            # Calculate gravity basing on polynomial and temperature with offset
            socket_message['gravity'] = socket_message['angle'] * result[2] + result[3]
            socket_message['temperature'] = socket_message['temperature'] + result[4]

            # Print data on screen
            self.l_labels[result[0]].config(text=result[0].replace('_', ' ').upper() + '\n' +
                                                 result[6] + '\n' +
                                                 'T: ' + '%.1f' % socket_message['temperature'] + '\n' +
                                                 'SG: ' + '%.3f' % socket_message['gravity'])

            # Send to database if log and update sparklines
            del socket_message['name']

            if result[5]:
                self.database.execute_fermentation(result[1], socket_message)
                self.f_sparklines[result[0]].update_sparklines()
