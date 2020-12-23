# Standard libraries
from tkinter import *
import csv
import datetime
from _collections import OrderedDict

# Imported libraries
from PIL import Image, ImageTk

# My libraries


class ISpindelTabGUI(Frame):
    """A class for iSpindel tab creation"""
    def __init__(self, tab_control, ispindel_parameters, database):
        super().__init__(tab_control)
        self.name = 'iSpindel'
        self.ispindel_parameters = ispindel_parameters
        self.database = database
        self.w_scale = 1.0
        self.h_scale = 1.0

        # Images for labels
        self.img_ispindel = Image.open('images/ispindel2.bmp')
        self.img_ispindel_copy = self.img_ispindel.copy()
        self.img_c_ispindel = ImageTk.PhotoImage(image=self.img_ispindel)

        # CATIA coordinates for GUI objects
        filename = 'data/ispindel_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.ispindel_coords = {}

            for row in reader:
                if row[0] == 'rect':
                    self.ispindel_rect = (int(row[1]), int(row[2]))
                else:
                    self.ispindel_coords[row[0]] = (int(row[1]), int(row[2]))

        # Names of GUI objects in the tab
        self.c_ispindel = Canvas(self)
        self.f_settings_parameters = Frame(self)
        self.l_status = Label(self, font=(None, 14), text='Waiting for data acquisition')

        # c_ispindel
        self.c_dots = {}
        self.c_lines = {}

        self.c_background = self.c_ispindel.create_image(0, 0, anchor=N + W, image=self.img_c_ispindel)

        # f_settings_parameters
        # f_settings
        self.entries_texts = ['Batch number',
                              'Fermentation vessel',
                              'Temperature offset',
                              'Gravity 1',
                              'Gravity 2',
                              ]

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
        self.parameters_values = OrderedDict.fromkeys(['measurement_time',
                                                       'angle',
                                                       'rssi',
                                                       'name',
                                                       'battery',
                                                       'temperature',
                                                       ])
        self.l_parameters_names = []
        self.l_parameters_values = []

        for i in range(len(self.parameters_values)):
            self.l_parameters_names.append(Label(self.f_settings_parameters, font=(None, 14), text=''))
            self.l_parameters_values.append(Label(self.f_settings_parameters, font=(None, 14), text=''))

        # Creating lists for looping
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

        # Setting rows and columns properties
        for i in range(3):
            self.columnconfigure(i, weight=1, uniform='column')

        for i in range(self.f_settings_parameters.grid_size()[1]):
            self.f_settings_parameters.rowconfigure(i, weight=1, uniform='row')

    def resize_image(self, event=None):
        # Getting scale
        width, height = event.width, event.height

        self.w_scale = width / self.img_ispindel.width
        self.h_scale = height / self.img_ispindel.height

        # Resizing images
        # img_ispindel
        image = self.img_ispindel_copy.resize((width, height))
        self.img_c_ispindel = ImageTk.PhotoImage(image)

        # Updating canvas
        self.c_ispindel.itemconfig(self.c_background, image=self.img_c_ispindel)

        # Updating coordinates of GUI objects
        if self.c_dots and self.c_lines:
            self.update_coordinates_of_dynamic_gui_objects()

    def update_coordinates_of_dynamic_gui_objects(self):
        for i, ispindel_coord_tuple in enumerate(self.ispindel_coords.items()):
            self.c_ispindel.coords(
                self.c_lines[ispindel_coord_tuple[0]],
                int(round(self.w_scale * self.img_ispindel.width * (ispindel_coord_tuple[1][0] /
                                                                    self.ispindel_rect[0]), 0)),
                int(round(self.h_scale * self.img_ispindel.height * (ispindel_coord_tuple[1][1] /
                                                                     self.ispindel_rect[1]), 0)),
                self.w_scale * self.img_ispindel.width / 3,
                self.l_parameters_names[i + 1].winfo_y() + self.l_parameters_names[i + 1].winfo_height() / 2)

            self.c_ispindel.coords(
                self.c_dots[ispindel_coord_tuple[0]],
                int(round(self.w_scale * (self.img_ispindel.width * (ispindel_coord_tuple[1][0] /
                                                                     self.ispindel_rect[0]) - 10), 0)),
                int(round(self.h_scale * (self.img_ispindel.height * (ispindel_coord_tuple[1][1] /
                                                                      self.ispindel_rect[1]) - 10), 0)),
                int(round(self.w_scale * (self.img_ispindel.width * (ispindel_coord_tuple[1][0] /
                                                                     self.ispindel_rect[0]) + 10), 0)),
                int(round(self.h_scale * (self.img_ispindel.height * (ispindel_coord_tuple[1][1] /
                                                                      self.ispindel_rect[1]) + 10), 0)))

    def socket_parameters_update(self, socket_message):
        self.l_status.config(text='Data processing')

        # Create dynamic GUI objects (dots, lines)
        if not self.c_dots and not self.c_lines:
            for k, v in self.ispindel_coords.items():
                self.c_dots[k] = self.c_ispindel.create_oval(
                    int(round(self.w_scale * (self.img_ispindel.width * (v[0] / self.ispindel_rect[0]) - 10), 0)),
                    int(round(self.h_scale * (self.img_ispindel.height * (v[1] / self.ispindel_rect[1]) - 10), 0)),
                    int(round(self.w_scale * (self.img_ispindel.width * (v[0] / self.ispindel_rect[0]) + 10), 0)),
                    int(round(self.h_scale * (self.img_ispindel.height * (v[1] / self.ispindel_rect[1]) + 10), 0)),
                    fill='black')

                self.c_lines[k] = self.c_ispindel.create_line(
                    int(round(self.w_scale * self.img_ispindel.width * (v[0] / self.ispindel_rect[0]), 0)),
                    int(round(self.h_scale * self.img_ispindel.height * (v[1] / self.ispindel_rect[1]), 0)),
                    int(round(self.w_scale * self.img_ispindel.width * (v[0] / self.ispindel_rect[0]), 0)),
                    int(round(self.h_scale * self.img_ispindel.height * (v[1] / self.ispindel_rect[1]), 0)),
                    width=2)

        # Draw lines in realtime
        difference = 1
        start = datetime.datetime.now()
        stop = start + datetime.timedelta(seconds=difference)

        while (stop - datetime.datetime.now()).total_seconds() >= 0:
            for i, ispindel_coord_tuple in enumerate(self.ispindel_coords.items()):
                xa = int(round(self.w_scale * (self.img_ispindel.width * (ispindel_coord_tuple[1][0] /
                                                                          self.ispindel_rect[0])), 0))
                ya = int(round(self.h_scale * (self.img_ispindel.height * (ispindel_coord_tuple[1][1] /
                                                                           self.ispindel_rect[1])), 0))
                xb = self.w_scale * self.img_ispindel.width / 3
                yb = self.l_parameters_names[i + 1].winfo_y() + self.l_parameters_names[i + 1].winfo_height() / 2
                a = (ya - yb) / (xa - xb)
                b = ya - a * xa
                x = xa + (xb - xa) * (1 - (stop - datetime.datetime.now()).total_seconds() / difference)
                y = a * x + b

                self.c_ispindel.coords(self.c_lines[ispindel_coord_tuple[0]], xa, ya, x, y)

            self.c_ispindel.update_idletasks()

        # Extract parameters (only to screen - there can be many socket readings, but not all end as parameters value)
        for k in self.parameters_values:
            if k in socket_message:
                self.parameters_values[k] = socket_message[k]

        # Extract parameters (to ispindel_parameters, not displayed on screen - saved for each socket reading)
        if 'temp_units' in socket_message:
            self.ispindel_parameters.parameters['temp_units'] = socket_message['temp_units']
        if 'interval' in socket_message:
            self.ispindel_parameters.parameters['interval'] = socket_message['interval']

        # Get temperature offset for iSpindel
        temperature_offset = self.database.get_ispindel_settings_temperature_offset(self.parameters_values['name'])

        if temperature_offset:
            self.e_temperature_offset.delete(0, END)
            self.e_temperature_offset.insert(0, temperature_offset)
            self.e_temperature_offset.config(fg='#000000')

        # Print socket data on the screen
        for i, parameter_value_tuple in enumerate(self.parameters_values.items()):
            if parameter_value_tuple[0] == 'rssi':
                self.l_parameters_names[i].config(text=parameter_value_tuple[0].upper())
            else:
                self.l_parameters_names[i].config(text=parameter_value_tuple[0].title())

            if parameter_value_tuple[0] == 'measurement_time':
                self.l_parameters_values[i].config(text=datetime.datetime.strftime(parameter_value_tuple[1],
                                                                                   '%Y-%m-%d %H:%M:%S'))
            else:
                self.l_parameters_values[i].config(text=parameter_value_tuple[1])

        self.l_status.config(text='Waiting for data acquisition')

    def entry_click(self, event):
        """Hide entry default text when focused"""
        for i, entry in enumerate(self.e_entries):
            if entry == event.widget and entry.get() == self.entries_texts[i]:
                entry.delete(0, END)
                entry.config(fg='#000000')
                break

    def entry_unclick(self, event):
        """Show entry default text when unfocused and left empty"""
        for i, entry in enumerate(self.e_entries):
            if entry == event.widget and not entry.get():
                entry.insert(END, self.entries_texts[i])
                entry.config(fg='#c5c5c5')
                break

    def save_calibration_point(self, event):
        try:
            for i, button in enumerate(self.b_calibration_points):
                if button == event.widget and self.e_entries[i + 3].get() and self.parameters_values['angle']:
                    gravity = float(self.e_entries[i + 3].get())
                    angle = self.parameters_values['angle']
                    self.ispindel_parameters.parameters['gravity_' + str(i)] = gravity
                    self.ispindel_parameters.parameters['angle_' + str(i)] = angle
                    self.l_calibration_points[i].config(text='Gravity: ' + '%.3f' % gravity +
                                                             ', angle: ' + '%.3f' % angle)
                    break
        except KeyError:
            pass
        except ValueError:
            pass
        except TypeError:
            pass

    def generate_polynomial(self, event):
        self.ispindel_parameters.calculate_polynomial()
        self.l_generate_polynomial.config(text='y = ' + str(round(self.ispindel_parameters.parameters['a'], 3)) +
                                               'x + ' + str(round(self.ispindel_parameters.parameters['b'], 3)))

    def confirm_settings(self, event):
        try:
            self.ispindel_parameters.parameters['batch_number'] = int(self.e_batch_number.get())
            self.ispindel_parameters.parameters['fermentation_vessel'] = self.e_fermentation_vessel.get()
            self.ispindel_parameters.parameters['ispindel_name'] = self.parameters_values['name']
            self.ispindel_parameters.parameters['temperature_offset'] = float(self.e_temperature_offset.get())
            self.ispindel_parameters.parameters['battery_notification'] = False
            self.ispindel_parameters.parameters['log'] = False

            self.database.execute_fermentation_settings(self.ispindel_parameters)
        except KeyError:
            pass
        except ValueError:
            pass
        except TypeError:
            pass

    def external_parameters_update(self, batch_number=None, og=None, batch_name=None, fermentation_vessel=None,
                                   fermentation_program=None):
        if batch_number:
            self.e_batch_number.delete(0, END)
            self.e_batch_number.insert(0, batch_number)
            self.e_batch_number.config(fg='#000000')

        if og:
            self.e_gravity_point_1.delete(0, END)
            self.e_gravity_point_1.insert(0, '1.000')
            self.e_gravity_point_1.config(fg='#000000')

            self.e_gravity_point_2.delete(0, END)
            self.e_gravity_point_2.insert(0, og)
            self.e_gravity_point_2.config(fg='#000000')

        if batch_name:
            self.ispindel_parameters.parameters['batch_name'] = batch_name

        if fermentation_vessel:
            self.e_fermentation_vessel.delete(0, END)
            self.e_fermentation_vessel.insert(0, fermentation_vessel)
            self.e_fermentation_vessel.config(fg='#000000')
            self.ispindel_parameters.parameters['fermentation_vessel'] = fermentation_vessel

        if fermentation_program:
            self.ispindel_parameters.parameters['fermentation_program'] = fermentation_program
