# Standard libraries
from tkinter import *

# Imported libraries

# My libraries
from graph_gui import GraphGUI


class GraphTabGUI(Frame):
    """A class for Graph tab creation"""
    def __init__(self, tab_control, database, dpi):
        super().__init__(tab_control)
        self.name = 'Graph'
        self.database = database
        self.dpi = dpi
        self.columns_max_quantity = 3
        self.rows_max_index = 0
        self.columns_max_index = 0
        self.graphs = []

    def add_graph(self):
        # Names of GUI objects in the tab
        self.graphs.append(GraphGUI(self, self.database, self.dpi))

        self.count_rows_and_columns()

        # Adding GUI objects to the grid
        self.graphs[-1].grid(row=int((len(self.graphs) - 1) / self.columns_max_quantity),
                             column=int((len(self.graphs) - 1) % self.columns_max_quantity), sticky=NSEW)

        self.set_rows_and_columns_properties()

    def count_rows_and_columns(self):
        self.rows_max_index = int((len(self.graphs) - 1) / self.columns_max_quantity)
        if self.rows_max_index == 0:
            self.columns_max_index = int((len(self.graphs) - 1) % self.columns_max_quantity)
        else:
            self.columns_max_index = self.columns_max_quantity - 1

    def remove_graph(self):
        remove_flag_found = False

        for i in range(len(self.graphs.copy())):
            if not remove_flag_found:
                # Searching until graph with remove_flag is found and removing it
                if self.graphs[i].remove_flag:
                    self.graphs[i].destroy()
                    del self.graphs[i]
                    self.count_rows_and_columns()
                    remove_flag_found = True
            else:
                # Moving graphs following removed graph one frame back (e.g. graph 3 moved to graph 2 position, etc.)
                self.graphs[i - 1].grid(row=int((i - 1) / self.columns_max_quantity),
                                        column=int((i - 1) % self.columns_max_quantity))

        self.set_rows_and_columns_properties()

    def set_rows_and_columns_properties(self):
        for i in range(self.grid_size()[0]):
            if i <= self.columns_max_index:
                self.columnconfigure(i, weight=1, uniform='column')
            else:
                self.columnconfigure(i, weight=0, uniform='')

        for i in range(self.grid_size()[1]):
            if i <= self.rows_max_index:
                self.rowconfigure(i, weight=1, uniform='row')
            else:
                self.rowconfigure(i, weight=0, uniform='')
