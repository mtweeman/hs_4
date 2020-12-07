# Standard libraries
from tkinter import *
from tkinter import ttk

# Imported libraries
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates

# My libraries


class GraphGUI(Frame):
    """A class for 'Graph' tab creation"""
    def __init__(self, graph_tab_gui, database, dpi):
        super().__init__(graph_tab_gui)
        self.graph_tab_gui = graph_tab_gui
        self.database = database
        self.dpi = dpi
        self.remove_flag = False

        # Names of GUI objects in the tab
        self.f_toolbar = Frame(self)
        self.f_navigation_toolbar = Frame(self.f_toolbar)
        self.cb_choice_1 = ttk.Combobox(self.f_toolbar, font=(None, 14), values=['Fermentation', 'Brewery'], state='readonly')
        self.cb_choice_1.set('Fermentation/Brewery data')
        self.batch_number = StringVar()
        self.cb_choice_2 = ttk.Combobox(self.f_toolbar, font=(None, 14), state='readonly')
        self.cb_choice_2.set('Batch number')
        self.column_1 = StringVar()
        self.cb_choice_3 = ttk.Combobox(self.f_toolbar, font=(None, 14), state='readonly')
        self.cb_choice_3.set('Values 1')
        self.column_2 = StringVar()
        self.cb_choice_4 = ttk.Combobox(self.f_toolbar, font=(None, 14), state='readonly')
        self.cb_choice_4.set('Values 2')
        self.l_button_off = Label(self.f_toolbar, font=(None, 14, 'bold'), fg='red', text='X')
        self.f_graph = Frame(self)

        # Adding GUI objects to the grid
        self.f_toolbar.grid(row=0, column=0, sticky=NSEW)
        self.f_navigation_toolbar.grid(row=0, column=0)
        self.cb_choice_1.grid(row=0, column=1, sticky=W + E)
        self.cb_choice_2.grid(row=0, column=2, sticky=W + E)
        self.cb_choice_3.grid(row=0, column=3, sticky=W + E)
        self.cb_choice_4.grid(row=0, column=4, sticky=W + E)
        self.l_button_off.grid(row=0, column=5, sticky=E)
        self.f_graph.grid(row=1, column=0, sticky=NSEW)

        # Adding commands to GUI objects
        self.cb_choice_1.bind('<<ComboboxSelected>>', self.load_tables)
        self.cb_choice_2.bind('<<ComboboxSelected>>', self.load_columns)
        self.cb_choice_3.bind('<<ComboboxSelected>>', self.load_column)
        self.cb_choice_4.bind('<<ComboboxSelected>>', self.load_column)
        self.l_button_off.bind('<Button-1>', self.remove_frame)

        # Setting rows and columns properties
        for i in range(self.grid_size()[0]):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(1, weight=1)

        for i in range(1, self.f_toolbar.grid_size()[0] - 1):
            self.f_toolbar.columnconfigure(i, weight=1, uniform='column')

        self.add_chart()

        # self.batch_number = self.database.get_tables()
        # self.cb_choice_2['values'] = self.batch_number

    def add_chart(self):
        # Names of figure objects in the tab
        self.fig = Figure(figsize=(3, 3), dpi=self.dpi)
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.f_graph)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.f_navigation_toolbar)

        # Figure and plot settings
        self.fig.set_facecolor('#f0f0f0')
        self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        self.fig.autofmt_xdate()
        self.ax1.set_ylabel('Values 1', fontsize=10)
        self.ax1.tick_params(axis=BOTH, labelsize=6)
        self.ax1.grid() # siatka w tle wykresu
        self.ax2.set_ylabel('Values 2', fontsize=10)
        self.ax2.tick_params(axis=BOTH, labelsize=6)
        self.ax2.grid()  # siatka w tle wykresu

        self.canvas.draw()
        self.toolbar.update()

        # Adding figure objects to the grid
        self.canvas.get_tk_widget().pack(expand=1, fill=BOTH)

    def remove_frame(self, event):
        self.remove_flag = True
        self.graph_tab_gui.remove_graph()

    def load_tables(self, event):
        self.batch_number = self.database.get_tables(self.cb_choice_1.get())
        self.cb_choice_2['values'] = self.batch_number

    def load_columns(self, event):
        self.column_1 = self.database.get_columns(self.cb_choice_2.get())
        self.column_2 = self.column_1.copy()
        self.cb_choice_3['values'] = self.column_1
        self.cb_choice_4['values'] = self.column_2

    def load_column(self, event):
        if event.widget == self.cb_choice_3:
            x, y = self.database.get_column(self.cb_choice_2.get(), self.cb_choice_3.get())
            self.ax1.plot(x, y, 'blue')
            self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            self.ax1.set_ylabel(self.cb_choice_3.get())
            self.canvas.draw()
        elif event.widget == self.cb_choice_4:
            x, y = self.database.get_column(self.cb_choice_2.get(), self.cb_choice_4.get())
            self.ax2.plot(x, y, 'red')
            self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            self.ax2.set_ylabel(self.cb_choice_4.get())
            self.canvas.draw()
