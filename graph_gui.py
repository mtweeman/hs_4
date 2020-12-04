# Standard libraries
from tkinter import *

# Imported libraries
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
        self.f_navigation_toolbar = Frame(self)
        self.f_graph = Frame(self)
        self.b_remove = Button(self, font=(None, 14), bg='red', text='-', command=self.remove_frame)

        # Adding GUI objects to the grid
        self.f_graph.grid(row=1, column=0, sticky=NSEW)
        self.f_navigation_toolbar.grid(row=0, column=0, sticky=W)
        self.b_remove.grid(row=0, column=0, sticky=E)

        # Setting rows and columns properties
        for i in range(self.grid_size()[0]):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(1, weight=1)

        self.ferm_chart()

    def ferm_chart(self):
    #     x, y = self.database.plot()
    #
        # Names of figure objects in the tab
        fig = Figure(figsize=(3, 3), dpi=self.dpi)
        plot = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=self.f_graph)
        toolbar = NavigationToolbar2Tk(canvas, self.f_navigation_toolbar)

        # Figure and plot settings
        fig.set_facecolor('#f0f0f0')
        fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        fig.autofmt_xdate(rotation=65)
        plot.set_ylabel('Y label', fontsize=14)
        plot.grid() # siatka w tle wykresu

        # Plot data
    #     plot.plot(x, y)
    #
        canvas.draw()
        toolbar.update()

        # Adding figure objects to the grid
        canvas.get_tk_widget().pack(expand=1, fill=BOTH)

    def remove_frame(self):
        self.remove_flag = True
        self.graph_tab_gui.remove_graph()
