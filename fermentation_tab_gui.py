# Standard libraries
from tkinter import *
from tkinter import ttk
import datetime

# Imported libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# My libraries


class FermentationTabGUI(Frame):
    """A class for 'Fermentation' tab creation"""
    def __init__(self, tab_control, fermentation_parameters, database, dpi):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=('None', '14'))
        self.fermentation_parameters = fermentation_parameters
        self.database = database
        self.dpi = dpi

        # Names of GUI objects in the tab
        self.f_parameters = Frame(self)
        self.f_navigation_toolbar = Frame(self)

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
        for i in range(4):
            self.columnconfigure(i, weight=1, uniform='column')

        for i in range(2):
            self.rowconfigure(i, weight=1, uniform='row')

        for i in range(self.f_parameters.grid_size()[1]):
            self.f_parameters.rowconfigure(i, weight=1, uniform='row')

        # Adding commands to GUI objects
        self.b_start.bind('<Button-1>', self.start)
        self.b_stop.bind('<Button-1>', self.stop)

    def start(self, event):
        self.fermentation_parameters.record_flag = True
        self.ferm_chart()

    def stop(self, event):
        self.fermentation_parameters.record_flag = False

    def update_parameters(self, socket_message):
        # Extract needed parameters into 'FermentationParameters' instance variable
        self.fermentation_parameters.parameters['measurement_time'] = datetime.datetime.now()

        for key, value in self.fermentation_parameters.parameters.items():
            if key in socket_message.keys():
                if key == 'angle' or key == 'battery' or key == 'temperature' or key == 'gravity':
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

            if parameter_value_tuple[0] == 'measurement_time':
                self.l_parameters_values[i].config(text=parameter_value_tuple[1].strftime('%Y-%m-%d %H:%M:%S'))
            else:
                self.l_parameters_values[i].config(text=parameter_value_tuple[1])

        # Save to database if record started
        if self.fermentation_parameters.record_flag:
            self.database.execute_fermentation(self.fermentation_parameters)

    def ferm_chart(self):
        # Names of figure objects in the tab
        fig = Figure(figsize=(1, 1), dpi=self.dpi)
        plot = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=self)
        toolbar = NavigationToolbar2Tk(canvas, self.f_navigation_toolbar)

        # Figure and plot settings
        fig.set_facecolor('#f0f0f0')
        plot.set_xlabel('X label', fontsize=14)
        plot.set_ylabel('Y label', fontsize=14)
        plot.grid()

        # Plot data
        y = [i ** 2 for i in range(101)]

        plot.plot(y)

        canvas.draw()
        toolbar.update()

        # Adding figure objects to the grid
        canvas.get_tk_widget().grid(row=0, column=1, columnspan=3, sticky=NSEW)
        self.f_navigation_toolbar.grid(row=1, column=1, sticky=N + W)
