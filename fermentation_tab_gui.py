# Standard libraries
from tkinter import *
from tkinter import ttk
import csv

# Imported libraries
from PIL import Image, ImageTk


class FermentationTabGUI(Frame):
    """A class for 'Fermentation' tab creation"""

    def __init__(self, tab_control, fermentation_parameters, database):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('None', '14'))
        self.fermentation_parameters = fermentation_parameters
        self.database = database

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
                self.f_frames[key] = Frame(self)
                self.l_labels[key] = Label(self.f_frames[key], font=(None, 14), text=key.replace('_', ' ').upper())
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
                                         anchor=CENTER)
                self.l_labels[key].grid(row=0, column=0)

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

    def update_parameters(self, socket_message):
        # Check for data logging by iSpindel
        db_log = self.database.get_ispindel_log(socket_message['name'])

        if db_log:
            print('zbieramy')

        # # Extract needed parameters into 'FermentationParameters' instance variable
        # self.fermentation_parameters.parameters['measurement_time'] = datetime.datetime.now()
        #
        # for key, value in self.fermentation_parameters.parameters.items():
        #     if key in socket_message.keys():
        #         if key == 'angle' or key == 'battery' or key == 'temperature' or key == 'gravity':
        #             self.fermentation_parameters.parameters[key] = float(socket_message[key])
        #         elif key == 'interval' or key == 'rssi':
        #             self.fermentation_parameters.parameters[key] = float(socket_message[key])
        #         else:
        #             self.fermentation_parameters.parameters[key] = socket_message[key]
        #
        # # Print socket data on the screen
        # for i, parameter_value_tuple in enumerate(self.fermentation_parameters.parameters.items()):
        #     if parameter_value_tuple[0] == 'rssi':
        #         self.l_parameters_names[i].config(text=parameter_value_tuple[0].upper())
        #     else:
        #         self.l_parameters_names[i].config(text=parameter_value_tuple[0].title())
        #
        #     if parameter_value_tuple[0] == 'measurement_time':
        #         self.l_parameters_values[i].config(text=parameter_value_tuple[1].strftime('%Y-%m-%d %H:%M:%S'))
        #     else:
        #         self.l_parameters_values[i].config(text=parameter_value_tuple[1])
        #
        # # Save to database if record started
        # if self.fermentation_parameters.record_flag:
        #     self.database.execute_fermentation(self.fermentation_parameters,
        #                                        self.ispindel_parameters.parameters['batch_number'],
        #                                        )
