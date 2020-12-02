# Standard libraries
from tkinter import *
from tkinter import ttk
import csv
import datetime
from _collections import OrderedDict

# Imported libraries
from PIL import Image, ImageTk

# My libraries


class ISpindelTabGUI(Frame):
    """A class for 'iSpindel' tab creation"""

    def __init__(self, tab_control, ispindel_parameters, database):
        super().__init__(tab_control)
        self.name = 'iSpindel'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('None', '14'))
        self.ispindel_parameters = ispindel_parameters
        self.database = database
        self.w_scale = 0.0
        self.h_scale = 0.0

        # Images for labels
        self.img_ispindel = Image.open('images/ispindel2.bmp')
        self.img_ispindel_copy = self.img_ispindel.copy()
        self.img_c_ispindel = ImageTk.PhotoImage(image=self.img_ispindel)

        # Names of GUI objects in the tab
        self.c_ispindel = Canvas(self)

        self.f_settings_parameters = Frame(self)

        self.l_status = Label(self, font=(None, 14), text='Waiting for data acquisition')

        # f_settings_parameters
        # f_settings
        self.entries_texts = ['Batch number',
                              'Fermentation vessel',
                              'Temperature offset',
                              'Gravity 1',
                              'Gravity 2']

        self.e_batch_number = Entry(self.f_settings_parameters, font=(None, 14), fg='#c5c5c5')
        self.e_batch_number.insert(END, self.entries_texts[0])
        self.e_fermentation_vessel = Entry(self.f_settings_parameters, font=(None, 14), fg='#c5c5c5')
        self.e_fermentation_vessel.insert(END, self.entries_texts[1])
        self.e_temperature_offset = Entry(self.f_settings_parameters, font=(None, 14), fg='#c5c5c5')
        self.e_temperature_offset.insert(END, self.entries_texts[2])
        self.e_gravity_point_1 = Entry(self.f_settings_parameters, font=(None, 14), fg='#c5c5c5')
        self.e_gravity_point_1.insert(END, self.entries_texts[3])
        self.e_gravity_point_2 = Entry(self.f_settings_parameters, font=(None, 14), fg='#c5c5c5')
        self.e_gravity_point_2.insert(END, self.entries_texts[4])
        self.b_calibration_point_1 = Button(
            self.f_settings_parameters, font=(None, 14), text='Calibration point 1', anchor=W)
        self.l_calibration_point_1 = Label(
            self.f_settings_parameters, font=(None, 14), text='')
        self.b_calibration_point_2 = Button(
            self.f_settings_parameters, font=(None, 14), text='Calibration point 2', anchor=W)
        self.l_calibration_point_2 = Label(
            self.f_settings_parameters, font=(None, 14), text='')
        self.b_generate_polynomial = Button(
            self.f_settings_parameters, font=(None, 14), text='Generate polynomial', anchor=W)
        self.l_generate_polynomial = Label(
            self.f_settings_parameters, font=(None, 14), text='')
        self.b_confirm_settings = Button(
            self.f_settings_parameters, font=(None, 14), text='Confirm settings', anchor=W)

        # f_parameters
        self.parameters_values = OrderedDict.fromkeys(['time', 'angle', 'rssi', 'name', 'battery', 'temperature'])
        self.l_parameters_names = []
        self.l_parameters_values = []

        for i in range(len(self.parameters_values)):
            self.l_parameters_names.append(Label(self.f_settings_parameters, font=(None, 14), text=''))
            self.l_parameters_values.append(Label(self.f_settings_parameters, font=(None, 14), text=''))

        # self.c_items = {}
        self.c_dots = {}
        self.c_lines = {}

        # CATIA coordinates
        self.ispindel_rect = (400, 225)
        filename = 'data/ispindel_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.ispindel_coords = {}

            for row in reader:
                self.ispindel_coords[row[0]] = (int(row[1]), int(row[2]))

        # Creating list with all entries for looping
        self.e_entries = [self.e_batch_number,
                          self.e_fermentation_vessel,
                          self.e_temperature_offset,
                          self.e_gravity_point_1,
                          self.e_gravity_point_2,
                          ]

        self.b_calibration_points = [self.b_calibration_point_1,
                                     self.b_calibration_point_2,
                                     ]

        self.l_calibration_points = [self.l_calibration_point_1,
                                     self.l_calibration_point_2,
                                     ]

        # Adding images to GUI objects
        self.c_background = self.c_ispindel.create_image(0, 0, anchor=N + W, image=self.img_c_ispindel)

        # Adding GUI objects to the grid
        self.c_ispindel.place(relwidth=1, relheight=1)

        self.f_settings_parameters.grid(row=0, column=1, sticky=NSEW)

        self.l_status.grid(row=0, column=0, sticky=N + W)

        # f_settings_parameters
        # f_settings
        self.e_batch_number.grid(row=0, column=0, sticky=NSEW)
        self.e_fermentation_vessel.grid(row=1, column=0, sticky=NSEW)
        self.e_temperature_offset.grid(row=2, column=0, sticky=NSEW)
        self.e_gravity_point_1.grid(row=3, column=0, sticky=NSEW)
        self.e_gravity_point_2.grid(row=4, column=0, sticky=NSEW)
        self.b_calibration_point_1.grid(row=5, column=0, sticky=NSEW)
        self.l_calibration_point_1.grid(row=5, column=1, sticky=W)
        self.b_calibration_point_2.grid(row=6, column=0, sticky=NSEW)
        self.l_calibration_point_2.grid(row=6, column=1, sticky=W)
        self.b_generate_polynomial.grid(row=7, column=0, sticky=NSEW)
        self.l_generate_polynomial.grid(row=7, column=1, sticky=W)
        self.b_confirm_settings.grid(row=8, column=0, sticky=NSEW)

        # f_parameters
        for i in range(len(self.parameters_values)):
            self.l_parameters_names[i].grid(row=9 + i, column=0, sticky=W)
            self.l_parameters_values[i].grid(row=9 + i, column=1, sticky=W)

        # Setting rows and columns properties
        for i in range(3):
            self.columnconfigure(i, weight=1, uniform='column')

        for i in range(self.f_settings_parameters.grid_size()[1]):
            self.f_settings_parameters.rowconfigure(i, weight=1, uniform='row')

        # Adding commands to GUI objects
        self.c_ispindel.bind('<Configure>', self.resize_image)

        self.e_batch_number.bind('<FocusIn>', self.entry_click)
        self.e_batch_number.bind('<FocusOut>', self.entry_unclick)
        self.e_fermentation_vessel.bind('<FocusIn>', self.entry_click)
        self.e_fermentation_vessel.bind('<FocusOut>', self.entry_unclick)
        self.e_temperature_offset.bind('<FocusIn>', self.entry_click)
        self.e_temperature_offset.bind('<FocusOut>', self.entry_unclick)
        self.e_gravity_point_1.bind('<FocusIn>', self.entry_click)
        self.e_gravity_point_1.bind('<FocusOut>', self.entry_unclick)
        self.e_gravity_point_2.bind('<FocusIn>', self.entry_click)
        self.e_gravity_point_2.bind('<FocusOut>', self.entry_unclick)
        self.b_calibration_point_1.bind('<Button-1>', self.save_calibration_point)
        self.b_calibration_point_2.bind('<Button-1>', self.save_calibration_point)
        self.b_generate_polynomial.bind('<Button-1>', self.generate_polynomial)
        self.b_confirm_settings.bind('<Button-1>', self.confirm_settings)

        # Initial resize for grabbing coordinates (crash if socket sends data before tab activation)
        # TO BE CODED

    def resize_image(self, event=None):
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
            for i, ispindel_coord_tuple in enumerate(self.ispindel_coords.items()):
                self.c_ispindel.coords(
                    self.c_lines[ispindel_coord_tuple[0]],
                    int(round(self.w_scale * self.img_ispindel.width * (int(ispindel_coord_tuple[1][0]) /
                                                                        self.ispindel_rect[0]), 0)),
                    int(round(self.h_scale * self.img_ispindel.height * (int(ispindel_coord_tuple[1][1]) /
                                                                         self.ispindel_rect[1]), 0)),
                    self.w_scale * self.img_ispindel.width / 3,
                    self.l_parameters_names[i + 1].winfo_y() + self.l_parameters_names[i + 1].winfo_height() / 2)
                self.c_ispindel.coords(
                    self.c_dots[ispindel_coord_tuple[0]],
                    int(round(self.w_scale * (self.img_ispindel.width * (int(ispindel_coord_tuple[1][0]) /
                                                                         self.ispindel_rect[0]) - 10), 0)),
                    int(round(self.h_scale * (self.img_ispindel.height * (int(ispindel_coord_tuple[1][1]) /
                                                                          self.ispindel_rect[1]) - 10), 0)),
                    int(round(self.w_scale * (self.img_ispindel.width * (int(ispindel_coord_tuple[1][0]) /
                                                                         self.ispindel_rect[0]) + 10), 0)),
                    int(round(self.h_scale * (self.img_ispindel.height * (int(ispindel_coord_tuple[1][1]) /
                                                                          self.ispindel_rect[1]) + 10), 0)))

    # def button_switch(self, key=None):
    #     self.brewery_parameters.verify_parameters(key)
    #
    #     for key, value in self.brewery_parameters.parameters.items():
    #         if self.brewery_parameters.parameters[key]:
    #             self.c_brewery.itemconfig(self.c_items[key], image=self.img_c_button_on)
    #         else:
    #             self.c_brewery.itemconfig(self.c_items[key], image=self.img_c_button_off)

    def update_parameters(self, socket_message):
        self.l_status.config(text='Data processing')

        # Draw dots and lines
        for key, value in self.ispindel_coords.items():
            self.c_ispindel.delete(key)

            self.c_dots[key] = self.c_ispindel.create_oval(
                int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0]) - 10), 0)),
                int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1]) - 10), 0)),
                int(round(self.w_scale * (self.img_ispindel.width * (value[0] / self.ispindel_rect[0]) + 10), 0)),
                int(round(self.h_scale * (self.img_ispindel.height * (value[1] / self.ispindel_rect[1]) + 10), 0)),
                fill='black', tags=key)

            self.c_lines[key] = self.c_ispindel.create_line(
                int(round(self.w_scale * self.img_ispindel.width * (value[0] / self.ispindel_rect[0]), 0)),
                int(round(self.h_scale * self.img_ispindel.height * (value[1] / self.ispindel_rect[1]), 0)),
                int(round(self.w_scale * self.img_ispindel.width * (value[0] / self.ispindel_rect[0]), 0)),
                int(round(self.h_scale * self.img_ispindel.height * (value[1] / self.ispindel_rect[1]), 0)),
                width=2, tags=key)

        # Draw lines in realtime
        difference = 1
        start = datetime.datetime.now()
        stop = start + datetime.timedelta(seconds=difference)

        while (stop - datetime.datetime.now()).total_seconds() >= 0:
            for i, ispindel_coord_tuple in enumerate(self.ispindel_coords.items()):
                xa = int(round(self.w_scale * (self.img_ispindel.width * (int(ispindel_coord_tuple[1][0]) /
                                                                          self.ispindel_rect[0])), 0))
                ya = int(round(self.h_scale * (self.img_ispindel.height * (int(ispindel_coord_tuple[1][1]) /
                                                                           self.ispindel_rect[1])), 0))
                xb = self.w_scale * self.img_ispindel.width / 3
                yb = self.l_parameters_names[i + 1].winfo_y() + self.l_parameters_names[i + 1].winfo_height() / 2
                a = (ya - yb) / (xa - xb)
                b = ya - a * xa
                x = xa + (xb - xa) * (1 - (stop - datetime.datetime.now()).total_seconds() / difference)
                y = a * x + b

                self.c_ispindel.coords(self.c_lines[ispindel_coord_tuple[0]],
                    int(round(self.w_scale * self.img_ispindel.width * (int(ispindel_coord_tuple[1][0]) /
                                                                        self.ispindel_rect[0]), 0)),
                    int(round(self.h_scale * self.img_ispindel.height * (int(ispindel_coord_tuple[1][1]) /
                                                                         self.ispindel_rect[1]), 0)),
                    x, y)

            self.c_ispindel.update_idletasks()

        # Extract needed parameters into 'iSpindelTabGUI' instance variable
        self.parameters_values['time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

        for key, value in self.parameters_values.items():
            if key in socket_message.keys():
                if key == 'angle' or key == 'battery' or key == 'temperature':
                    self.parameters_values[key] = float(socket_message[key])
                else:
                    self.parameters_values[key] = socket_message[key]

        # Print socket data on the screen
        for i, parameter_value_tuple in enumerate(self.parameters_values.items()):
            if parameter_value_tuple[0] == 'rssi':
                self.l_parameters_names[i].config(text=parameter_value_tuple[0].upper())
            else:
                self.l_parameters_names[i].config(text=parameter_value_tuple[0].title())
            self.l_parameters_values[i].config(text=parameter_value_tuple[1])

        db_temperature_offset = self.database.get_ispindel_temperature_offset(self.parameters_values['name'])

        if db_temperature_offset:
            self.e_temperature_offset.delete(0, END)
            self.e_temperature_offset.insert(0, db_temperature_offset)
            self.e_temperature_offset.config(fg='#000000')

        self.l_status.config(text='Waiting for data acquisition')

    def entry_click(self, event):
        """Hide entry default text when focused"""
        for i, element in enumerate(self.e_entries):
            if element == event.widget and element.get() == self.entries_texts[i]:
                element.delete(0, END)
                element.config(fg='#000000')

    def entry_unclick(self, event):
        """Show entry default text when unfocused and left empty"""
        for i, element in enumerate(self.e_entries):
            if element == event.widget and not element.get():
                element.insert(END, self.entries_texts[i])
                element.config(fg='#c5c5c5')

    def save_calibration_point(self, event):
        try:
            for i, element in enumerate(self.b_calibration_points):
                if element == event.widget:
                    gravity = float(self.e_entries[i + 3].get())
                    angle = self.parameters_values['angle']
                    self.ispindel_parameters.parameters['gravity_' + str(i)] = gravity
                    self.ispindel_parameters.parameters['angle_' + str(i)] = angle
                    self.l_calibration_points[i].config(text='Gravity: ' + '%.3f' % gravity +
                                                             ', angle: ' + '%.3f' % angle)
        except KeyError:
            pass
        except ValueError:
            pass
        except TypeError:
            pass

    def generate_polynomial(self, event):
        try:
            self.ispindel_parameters.calculate_polynomial()
            self.l_generate_polynomial.config(text='y = ' + str(round(self.ispindel_parameters.parameters['a'], 3)) +
                                                   'x + ' + str(round(self.ispindel_parameters.parameters['b'], 3)))
        except TypeError:
            pass

    def confirm_settings(self, event):
        self.ispindel_parameters.parameters['batch_number'] = int(self.e_batch_number.get())
        self.ispindel_parameters.parameters['fermentation_vessel'] = self.e_fermentation_vessel.get()
        self.ispindel_parameters.parameters['ispindel_name'] = self.parameters_values['name']
        self.ispindel_parameters.parameters['temperature_offset'] = float(self.e_temperature_offset.get())
        self.ispindel_parameters.parameters['battery_notification'] = False
        self.ispindel_parameters.parameters['log'] = False

        self.database.execute_fermentation_settings(self.ispindel_parameters)

    def recipe_parameters_update(self, batch_number, og):
        self.e_batch_number.delete(0, END)
        self.e_batch_number.insert(0, batch_number)
        self.e_batch_number.config(fg='#000000')

        self.e_gravity_point_1.delete(0, END)
        self.e_gravity_point_1.insert(0, '1.000')
        self.e_gravity_point_1.config(fg='#000000')

        self.e_gravity_point_2.delete(0, END)
        self.e_gravity_point_2.insert(0, og)
        self.e_gravity_point_2.config(fg='#000000')

    def fermentation_vessel_update(self, fermentation_vessel):
        self.e_fermentation_vessel.delete(0, END)
        self.e_fermentation_vessel.insert(0, fermentation_vessel)
        self.e_fermentation_vessel.config(fg='#000000')
