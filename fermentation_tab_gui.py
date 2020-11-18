# Standard libraries
from tkinter import *
from tkinter import ttk
from _collections import OrderedDict
import datetime

# Imported libraries

# My libraries


class FermentationTabGUI(Frame):
    """A class for 'Fermentation' tab creation"""
    def __init__(self, tab_control, fermentation_parameters, database):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('None', '14'))
        self.fermentation_parameters = fermentation_parameters
        self.database = database

        # Names of GUI objects in the tab
        self.f_parameters = Frame(self, relief=SOLID)

        self.b_start = Button(self.f_parameters, font=(None, 14), text='Start', anchor=W)
        self.b_stop = Button(self.f_parameters, font=(None, 14), text='Stop', anchor=W)

        self.l_parameters_names = []
        self.l_parameters_values = []

        for i in range(len(self.fermentation_parameters.parameters)):
            self.l_parameters_names.append(Label(self.f_parameters, font=(None, 14), text=''))
            self.l_parameters_values.append(Label(self.f_parameters, font=(None, 14), text=''))

        # Adding GUI objects to the grid
        self.f_parameters.grid(row=0, column=0, sticky=NSEW)

        self.b_start.grid(row=0, column=0, sticky=NSEW)
        self.b_stop.grid(row=1, column=0, sticky=NSEW)

        for i in range(len(self.fermentation_parameters.parameters)):
            self.l_parameters_names[i].grid(row=2 + i, column=0, sticky=W)
            self.l_parameters_values[i].grid(row=2 + i, column=1, sticky=W)

        # Setting rows and columns properties
        for i in range(self.f_parameters.grid_size()[1]):
            self.f_parameters.rowconfigure(i, weight=1, uniform='row')

        # Adding commands to GUI objects
        self.b_start.bind('<Button-1>', self.start)
        self.b_stop.bind('<Button-1>', self.stop)

    def start(self, event):
        print('start')

    def stop(self, event):
        print('stpo')

    def update_parameters(self, socket_message):
        # Extract needed parameters into 'FermentationParameters' instance variable
        self.fermentation_parameters.parameters['time'] = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

        for key, value in self.fermentation_parameters.parameters.items():
            if key in socket_message.keys():
                if key == 'angle' or key == 'battery' or key == 'temperature':
                    self.fermentation_parameters.parameters[key] = float(socket_message[key])
                elif key == 'interval' or key == 'rssi':
                    self.fermentation_parameters.parameters[key] = float(socket_message[key])
                else:
                    self.fermentation_parameters.parameters[key] = socket_message[key]

        # Print socket data on the screen
        for i, parameter_value_tuple in enumerate(self.fermentation_parameters.parameters.items()):
            if parameter_value_tuple[0] == 'rssi':
                self.l_parameters_names[i].config(text=parameter_value_tuple[0].upper())
            else:
                self.l_parameters_names[i].config(text=parameter_value_tuple[0].title())
            self.l_parameters_values[i].config(text=parameter_value_tuple[1])
