# Standard libraries
from tkinter import *
from tkinter import ttk

# Imported libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates

# My libraries


class GraphGUI(Frame):
    """A class for Graph creation"""
    def __init__(self, graph_tab_gui, database, dpi):
        super().__init__(graph_tab_gui)
        self.graph_tab_gui = graph_tab_gui
        self.database = database
        self.dpi = dpi
        self.remove_flag = False
        self.ax1 = None
        self.ax2 = None
        self.batch_number = ''
        self.column_1 = ''
        self.column_2 = ''

        # Names of GUI objects in the tab
        self.f_toolbar = Frame(self)
        self.f_graph = Frame(self)

        # f_toolbar
        self.f_navigation_toolbar = Frame(self.f_toolbar)
        self.cb_choice_0 =\
            ttk.Combobox(self.f_toolbar, font=(None, 14), values=['Fermentation', 'Brewery'], state='readonly')
        self.cb_choice_1 = ttk.Combobox(self.f_toolbar, font=(None, 14), state='readonly')
        self.cb_choice_2 = ttk.Combobox(self.f_toolbar, font=(None, 14), state='readonly')
        self.cb_choice_3 = ttk.Combobox(self.f_toolbar, font=(None, 14), state='readonly')
        self.l_button_off = Label(self.f_toolbar, font=(None, 14, 'bold'), fg='red', text='X')

        # Creating lists for looping
        self.cb_choices = [self.cb_choice_0,
                           self.cb_choice_1,
                           self.cb_choice_2,
                           self.cb_choice_3,
                           ]

        self.cb_texts = ['Fermentation/Brewery data',
                         'Batch number',
                         'Values 1',
                         'Values 2',
                         ]

        for i in range(len(self.cb_texts) - 1):
            self.cb_choices[i].set(self.cb_texts[i])

        # Adding GUI objects to the grid
        self.f_toolbar.grid(row=0, column=0, sticky=NSEW)
        self.f_graph.grid(row=1, column=0, sticky=NSEW)

        # f_toolbar
        self.f_navigation_toolbar.grid(row=0, column=0)
        self.cb_choice_0.grid(row=0, column=1, sticky=W + E)
        self.cb_choice_1.grid(row=0, column=2, sticky=W + E)
        self.cb_choice_2.grid(row=0, column=3, sticky=W + E)
        self.cb_choice_3.grid(row=0, column=4, sticky=W + E)
        self.l_button_off.grid(row=0, column=5, sticky=E)

        # Adding commands to GUI objects
        self.cb_choice_0.bind('<<ComboboxSelected>>', self.load_tables)
        self.cb_choice_1.bind('<<ComboboxSelected>>', self.load_columns)
        self.cb_choice_2.bind('<<ComboboxSelected>>', self.load_column)
        self.cb_choice_3.bind('<<ComboboxSelected>>', self.load_column)
        self.l_button_off.bind('<Button-1>', self.remove_frame)

        # Setting rows and columns properties
        for i in range(self.grid_size()[0]):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(1, weight=1)

        for i in range(1, self.f_toolbar.grid_size()[0] - 1):
            self.f_toolbar.columnconfigure(i, weight=1, uniform='column')

    def add_plot(self, x, y, label):
        if not self.ax1:
            # Names of figure objects in the tab
            self.fig = Figure(figsize=(1, 1), dpi=self.dpi)

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.f_graph)
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.f_navigation_toolbar)

            self.fig.set_facecolor('#f0f0f0')

            self.ax1 = self.fig.add_subplot(111)
            self.line1, = self.ax1.plot(x, y, 'blue')

            # Adding figure objects to the grid
            self.canvas.get_tk_widget().pack(expand=1, fill=BOTH)
        else:
            self.ax2 = self.ax1.twinx()
            self.line2, = self.ax2.plot(x, y, 'red')

        # Figure settings
        self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        self.fig.autofmt_xdate()
        self.fig.gca().set_ylabel(label)
        if not self.ax2:
            self.fig.gca().tick_params(axis=BOTH, labelsize=6)
        else:
            self.fig.gca().tick_params(axis=Y, labelsize=6)
        self.fig.gca().autoscale(tight=True)
        self.fig.gca().grid()

        self.canvas.draw()
        self.toolbar.update()

        # Adding commands to GUI objects
        self.fig.canvas.mpl_connect('button_press_event', self.activate_other_plot)

    def activate_other_plot(self, event):
        if event.button == 1:
            self.ax1.set_zorder(0)
            if self.ax2:
                self.ax2.set_zorder(-100)
        elif event.button == 3 and self.ax2:
            self.ax1.set_zorder(-100)
            self.ax2.set_zorder(0)

    def remove_frame(self, event):
        self.remove_flag = True
        self.graph_tab_gui.remove_graph()

    def set_texts_and_choices(self, start, choices):
        for i in range(start, len(self.cb_texts)):
            # Set displayed text
            # i < len(self.cb_text) is passed by all values except maximum self.cb_choices index
            # i == start condition is passed even by maximum self.cb_choices index
            if i < len(self.cb_texts) - 1 or i == start:
                if self.cb_choices[i].get() != self.cb_texts[i]:
                    self.cb_choices[i].set(self.cb_texts[i])
            else:
                if self.cb_choices[i].get():
                    self.cb_choices[i].set('')

            # Set values for choices
            if i == start:
                if choices:
                    self.cb_choices[i]['values'] = choices
                else:
                    if self.cb_choices[i]['values']:
                        self.cb_choices[i]['values'] = ''
            else:
                if self.cb_choices[i]['values']:
                    self.cb_choices[i]['values'] = ''

    def load_tables(self, event):
        # Load tables
        self.batch_number = self.database.get_tables(self.cb_choice_0.get())

        # Set texts and choices for choices to be made (load_tables is for cb_choice_0, therefore value is for 1)
        self.set_texts_and_choices(1, self.batch_number)

        # Update plots
        if self.ax1:
            self.update_plot('1')

        if self.ax2:
            self.update_plot('2')

    def load_columns(self, event=None):
        if event:
            # Load columns
            self.column_1 = self.database.get_columns(self.cb_choice_1.get())

            # Set texts and choices for choices to be made (load_columns is for cb_choice_1, therefore value is for 2)
            self.set_texts_and_choices(2, self.column_1)

            # Update plots
            if self.ax1:
                self.update_plot('1')

            if self.ax2:
                self.update_plot('2')
        else:
            # Load columns
            self.column_2 = self.database.get_columns(self.cb_choice_1.get())

            # Set texts and choices for choices to be made (load_columns is for cb_choice_1, therefore value is for 3)
            self.set_texts_and_choices(3, self.column_2)

    def load_column(self, event):
        if event.widget == self.cb_choice_2:
            x, y = self.database.get_column(self.cb_choice_1.get(), self.cb_choice_2.get())
            if not self.ax1:
                self.add_plot(x, y, self.cb_choice_2.get())
            else:
                self.update_plot('1', x, y)

            # Values only reloaded when load_columns executed as it can result in different set of columns
            if not self.cb_choice_3['values']:
                self.load_columns()

        elif event.widget == self.cb_choice_3:
            x, y = self.database.get_column(self.cb_choice_1.get(), self.cb_choice_3.get())
            if not self.ax2:
                self.add_plot(x, y, self.cb_choice_3.get())
            else:
                self.update_plot('2', x, y)

    def update_plot(self, plot, x=None, y=None):
        if plot == '1':
            self.line1.set_data(x, y)
            self.ax1.set_ylabel(self.cb_choice_2.get())
        elif plot == '2':
            self.line2.set_data(x, y)
            self.ax2.set_ylabel(self.cb_choice_3.get())

        for plt in self.fig.get_axes():
            plt.relim()
            plt.autoscale()

        self.canvas.draw()
