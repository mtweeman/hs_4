# Standard libraries
from tkinter import *

# Imported libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

# My libraries


class SparklinesGUI(Frame):
    """A class for Sparklines creation"""
    def __init__(self, f_frame, database, dpi):
        super().__init__(f_frame)
        self.database = database
        self.dpi = dpi
        self.batch_number = None
        self.ax1 = None
        self.ax2 = None

        self.add_sparklines()

    def add_sparklines(self):
        # Names of figure objects in the tab
        self.fig = Figure(figsize=(1, 1), dpi=self.dpi)
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()

        self.line1, = self.ax1.plot(0, 0, 'blue')
        self.line2, = self.ax2.plot(0, 0, 'red')

        # Adding figure objects to the grid
        self.canvas.get_tk_widget().pack(expand=1, fill=BOTH)

        # Figure settings
        for plt in self.fig.get_axes():
            plt.autoscale(tight=True)
            plt.get_xaxis().set_visible(False)
            plt.get_yaxis().set_visible(False)

        self.canvas.draw()

    def update_sparklines(self, batch_number=None):
        if batch_number:
            self.batch_number = str(batch_number) + '_Ferm'

        x1, y1 = self.database.get_column(self.batch_number, 'gravity')
        x2, y2 = self.database.get_column(self.batch_number, 'temperature')
        self.line1.set_data(x1, y1)
        self.line2.set_data(x2, y2)

        for plt in self.fig.get_axes():
            plt.relim()
            plt.autoscale()

        self.canvas.draw_idle()

    def clear_sparklines(self):
        self.line1.set_data(0, 0)
        self.line2.set_data(0, 0)

        self.canvas.draw_idle()
