# Standard libraries
from tkinter import *
import csv

# Imported libraries
from PIL import Image, ImageTk

# My libraries
from sparklines_gui import SparklinesGUI


class FermentationTabGUI(Frame):
    """A class for Fermentation tab creation"""
    def __init__(self, tab_control, fermentation_parameters, database, dpi):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.fermentation_parameters = fermentation_parameters
        self.database = database
        self.dpi = dpi
        self.w_scale = 1.0
        self.h_scale = 1.0

        # Images for labels
        self.img_fermentation = Image.open('images/ferm4.bmp')
        self.img_toggle_on = Image.open('images/toggle_on.png')
        self.img_toggle_off = Image.open('images/toggle_off.png')
        self.img_button_on = Image.open('images/button_on.png')
        self.img_button_off = Image.open('images/button_off.png')

        self.img_toggle_on = self.img_toggle_on.resize((60, 38))
        self.img_toggle_off = self.img_toggle_off.resize((60, 38))
        self.img_button_on = self.img_button_on.resize((32, 32))
        self.img_button_off = self.img_button_off.resize((32, 32))

        self.img_fermentation_copy = self.img_fermentation.copy()
        self.img_toggle_on_copy = self.img_toggle_on.copy()
        self.img_toggle_off_copy = self.img_toggle_off.copy()
        self.img_button_on_copy = self.img_button_on.copy()
        self.img_button_off_copy = self.img_button_off.copy()

        self.img_c_fermentation = ImageTk.PhotoImage(image=self.img_fermentation)
        self.img_c_toggle_on = ImageTk.PhotoImage(image=self.img_toggle_on)
        self.img_c_toggle_off = ImageTk.PhotoImage(image=self.img_toggle_off)
        self.img_c_button_on = ImageTk.PhotoImage(image=self.img_button_on)
        self.img_c_button_off = ImageTk.PhotoImage(image=self.img_button_off)

        # CATIA coordinates for GUI objects
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.fermentation_coords = {}

            for row in reader:
                if row[0] == 'rect':
                    self.fermentation_rect = (int(row[1]), int(row[2]))
                else:
                    self.fermentation_coords[row[0]] = (int(row[1]), int(row[2]))

        # Names of GUI objects in the tab
        self.c_fermentation = Canvas(self)

        # c_fermentation
        self.c_items = {}  # buttons and toggles
        self.f_frames = {}
        self.l_labels = {}
        self.f_sparklines = {}
        self.c_background = self.c_fermentation.create_image(0, 0, anchor=N + W, image=self.img_c_fermentation)

        for k, v in self.fermentation_coords.items():
            if 'fv' in k or 'master' in k:
                # Toggles
                self.c_items[k] = self.c_fermentation.create_image(
                    int(round(self.w_scale * self.img_fermentation.width * (v[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.h_scale * self.img_fermentation.height * (v[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_toggle_off)

                # Frames assosciated with fermentation vessels
                if 'fv' in k:
                    self.f_frames[k] = Frame(self)
                    self.l_labels[k] = Label(
                        self.f_frames[k], fg='white', bg='#555555', font=(None, 14), text=k.replace('_', ' ').upper())
                    self.f_sparklines[k] = SparklinesGUI(self.f_frames[k], self.database, self.dpi)
            else:
                # Buttons
                self.c_items[k] = self.c_fermentation.create_image(
                    int(round(self.w_scale * self.img_fermentation.width * (v[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.h_scale * self.img_fermentation.height * (v[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_button_off)

        # Adding GUI objects to the grid
        self.c_fermentation.place(relwidth=1, relheight=1)

        for k, v in self.fermentation_coords.items():
            if 'fv' in k:
                self.f_frames[k].place(relx=v[0] / self.fermentation_rect[0],
                                       rely=(v[1] + self.img_toggle_on.height) / self.fermentation_rect[1],
                                       relwidth=0.1,
                                       relheight=0.2,
                                       anchor=N)
                self.l_labels[k].grid(row=0, column=0, sticky=NSEW)
                self.f_sparklines[k].grid(row=1, column=0, sticky=NSEW)

                # Check fermentation vessel for log = True
                # if condition is correct, update sparklines (so far only empty figure)
                batch_number = self.database.get_fermentation_settings_batch_number(k)
                if batch_number:
                    self.f_sparklines[k].update_sparklines(batch_number)

        # Adding commands to GUI objects
        self.c_fermentation.bind('<Configure>', self.resize_image)

        for k in self.fermentation_coords:
            self.c_fermentation.tag_bind(self.c_items[k], '<Button-1>', lambda event, key=k: self.toggle_switch(key))

        # Setting rows and columns properties
        for k in self.f_frames:
            self.f_frames[k].columnconfigure(0, weight=1)
            self.f_frames[k].rowconfigure(1, weight=1)

    def resize_image(self, event):
        # Getting scale
        width, height = event.width, event.height

        self.w_scale = width / self.img_fermentation.width
        self.h_scale = height / self.img_fermentation.height

        # Resizing images
        # img_brewery
        image = self.img_fermentation_copy.resize((width, height))
        self.img_c_fermentation = ImageTk.PhotoImage(image)

        # img_toggle_on
        image = self.img_toggle_on_copy.resize(
            (int(round(self.w_scale * self.img_toggle_on.width, 0)),
             int(round(self.h_scale * self.img_toggle_on.height, 0))))
        self.img_c_toggle_on = ImageTk.PhotoImage(image)

        # img_toggle_off
        image = self.img_toggle_off_copy.resize(
            (int(round(self.w_scale * self.img_toggle_off.width, 0)),
             int(round(self.h_scale * self.img_toggle_off.height, 0))))
        self.img_c_toggle_off = ImageTk.PhotoImage(image)

        # img_button_on
        image = self.img_button_on_copy.resize(
            (int(round(self.w_scale * self.img_button_on.width, 0)),
             int(round(self.h_scale * self.img_button_on.height, 0))))
        self.img_c_button_on = ImageTk.PhotoImage(image)

        # img_button_off
        image = self.img_button_off_copy.resize(
            (int(round(self.w_scale * self.img_button_off.width, 0)),
             int(round(self.h_scale * self.img_button_off.height, 0))))
        self.img_c_button_off = ImageTk.PhotoImage(image)

        # Updating canvas
        self.c_fermentation.itemconfig(self.c_background, image=self.img_c_fermentation)
        self.update_toggles_and_buttons()

        # Updating coordinates of GUI objects
        for k, v in self.fermentation_coords.items():
            self.c_fermentation.coords(self.c_items[k],
                                       int(round(self.w_scale * self.img_fermentation.width *
                                                 (v[0] / self.fermentation_rect[0]), 0)),
                                       int(round(self.h_scale * self.img_fermentation.height *
                                                 (v[1] / self.fermentation_rect[1]), 0)))

    def update_toggles_and_buttons(self):
        for k in self.fermentation_parameters.parameters:
            if 'fv' in k or 'master' in k:
                if self.fermentation_parameters.parameters[k]:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_toggle_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_toggle_off)
            else:
                if self.fermentation_parameters.parameters[k]:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_button_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_button_off)

    def toggle_switch(self, key):
        self.fermentation_parameters.verify_parameters(key)
        self.update_toggles_and_buttons()

        # only for visual purposes - no delay for toggle/button to switch
        # otherwise it waits until function is finished
        self.c_fermentation.update_idletasks()

        # Updating database
        if 'fv' in key:
            self.database.execute_fermentation_settings_log(key, self.fermentation_parameters.parameters[key])
        elif 'master' in key:
            if self.fermentation_parameters.parameters[key]:
                ispindel_name = self.database.get_fermentation_settings_ispindel_name(key.replace('master', 'fv'))
                self.database.execute_ispindel_settings_master(ispindel_name)
            else:
                self.database.execute_ispindel_settings_master()

        # Updating data on screen
        if 'fv' in key:
            if (not self.fermentation_parameters.parameters[key] and
                    not self.fermentation_parameters.parameters[key.replace('fv', 'master')]):
                self.l_labels[key].config(text=key.replace('_', ' ').upper())
                self.f_sparklines[key].clear_sparklines()
            else:
                batch_number = self.database.get_fermentation_settings_batch_number(key)
                if batch_number:
                    self.f_sparklines[key].update_sparklines(batch_number)
        elif 'master' in key:
            if (not self.fermentation_parameters.parameters[key] and
                    not self.fermentation_parameters.parameters[key.replace('master', 'fv')]):
                self.l_labels[key.replace('master', 'fv')].config(text=key.replace('master_', 'fv ').upper())
                self.f_sparklines[key.replace('master', 'fv')].clear_sparklines()

    def socket_parameters_update(self, socket_message):
        # Checking if log = True for fermentation_vessel OR master
        result = self.database.get_fermentation_settings(socket_message['name'], True)
        if not result:
            result = self.database.get_fermentation_settings(socket_message['name'], False)

        if result:
            # Calculating gravity basing on polynomial and temperature with offset
            socket_message['gravity'] = socket_message['angle'] * result[2] + result[3]
            socket_message['temperature'] = socket_message['temperature'] + result[4]

            # Updating database and sparklines if log = True
            del socket_message['name']

            if result[5]:
                self.database.execute_fermentation(result[1], socket_message)
                self.f_sparklines[result[0]].update_sparklines()

            # Updating data on screen
            self.l_labels[result[0]].config(text=result[0].replace('_', ' ').upper() + '\n' +
                                                 result[6] + '\n' +
                                                 'T: ' + '%.1f' % socket_message['temperature'] + '\n' +
                                                 'SG: ' + '%.3f' % socket_message['gravity'])
