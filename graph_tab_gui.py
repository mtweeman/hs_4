# Standard libraries
from tkinter import *
from tkinter import ttk

# Imported libraries


# My libraries
from graph_gui import GraphGUI


class GraphTabGUI(Frame):
    """A class for 'Graph' tab creation"""
    def __init__(self, tab_control, database, dpi):
        super().__init__(tab_control)
        self.name = 'Graph'
        self.database = database
        self.dpi = dpi
        self.row_max = 2
        self.rows_quantity = 0
        self.columns_quantity = 0
        self.graphs = []

    def add_graph(self):
        # Names of GUI objects in the tab
        self.graphs.append(GraphGUI(self, self.database, self.dpi))

        self.count_rows_columns()

        # Adding GUI objects to the grid
        self.graphs[-1].grid(row=int((len(self.graphs) - 1) / self.row_max), column=int((len(self.graphs) - 1) % self.row_max), sticky=NSEW)

        self.set_rows_columns_properties()

    def count_rows_columns(self):
        self.rows_quantity = int((len(self.graphs) - 1) / self.row_max)
        if self.rows_quantity == 0:
            self.columns_quantity = int((len(self.graphs) - 1) % self.row_max)
        else:
            self.columns_quantity = 2

    def remove_graph(self):
        remove_flag_found = False

        for i in range(len(self.graphs.copy())):
            if not remove_flag_found:
                if self.graphs[i].remove_flag:
                    self.graphs[i].destroy()
                    del self.graphs[i]
                    self.count_rows_columns()
                    remove_flag_found = True
            else:
                self.graphs[i - 1].grid(row=int((i - 1) / self.row_max), column=int((i - 1) % self.row_max))

        self.set_rows_columns_properties()

    def set_rows_columns_properties(self):
        # Setting rows and columns properties
        for i in range(self.grid_size()[0]):
            if i <= self.columns_quantity:
                self.columnconfigure(i, weight=1, uniform='column')
            else:
                self.columnconfigure(i, weight=0, uniform='')

        for i in range(self.grid_size()[1]):
            if i <= self.rows_quantity:
                self.rowconfigure(i, weight=1, uniform='row')
            else:
                self.rowconfigure(i, weight=0, uniform='')
