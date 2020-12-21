# Standard libraries
from tkinter import *
from tkinter import ttk
from ctypes import windll

# Imported libraries
from PIL import Image

# My libraries
from recipe_tab_gui import RecipeTabGUI
from brewery_tab_gui import BreweryTabGUI
from ispindel_tab_gui import ISpindelTabGUI
from fermentation_tab_gui import FermentationTabGUI
from graph_tab_gui import GraphTabGUI
from add_graph_tab_gui import AddGraphTabGUI
from recipe_parameters import RecipeParameters
from brewery_parameters import BreweryParameters
from ispindel_parameters import ISpindelParameters
from fermentation_parameters import FermentationParameters
from socket_thread import SocketThread
from database import Database


def add_graph_to_graph_tab_gui(event):
    # Add graph to GraphTabGUI instance when AddGraphTabGUI tab was clicked
    if tab_control.tab(tab_control.select())['text'] == add_graph_tab_gui.name:
        graph_tab_gui.add_graph()
        tab_control.select(graph_tab_gui)


# Input
version = 4.01
icon = 'images/icon.ico'
image_brewery = Image.open('images/test7.bmp')
title_str = 'Hajle Silesia Homebrewing System '

# Create instances for parameter/database classes except for Threading classes
database = Database()
recipe_parameters = RecipeParameters()
brewery_parameters = BreweryParameters()
ispindel_parameters = ISpindelParameters()
fermentation_parameters = FermentationParameters(database)

# Window setup
windll.shcore.SetProcessDpiAwareness(1)  # no blur of fonts - NOT WORKING
windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')

root = Tk()
root.minsize(image_brewery.width, image_brewery.height)
root.state('zoomed')
# root.wm_state('iconic')
root.iconbitmap(icon)
root.title(title_str + str(version))
dpi = root.winfo_fpixels('1i')

# Style setup
style = ttk.Style()
style.theme_create('hs_theme', parent='classic', settings={'TNotebook': {'configure': {'background': '#888888'}},
                                                           'TNotebook.Tab': {'configure': {'background': '#555555',
                                                                                           'foreground': 'white',
                                                                                           'padding': [10, 10],
                                                                                           'font': (None, 14)},
                                                                             'label': {'side': ''},
                                                                             'map': {'background': [
                                                                                 ('selected', '#ffffff')],
                                                                                 'foreground': [
                                                                                     ('selected', 'black')]}},
                                                           'TCombobox': {'configure': {'arrowsize': 50}}})
style.theme_use('hs_theme')

# Tabs setup
tab_control = ttk.Notebook(root)
tab_control.pack(fill='both', expand=1)

ispindel_tab_gui = ISpindelTabGUI(tab_control, ispindel_parameters, database)
recipe_tab_gui = RecipeTabGUI(tab_control, recipe_parameters, ispindel_tab_gui, fermentation_parameters,
                              ispindel_parameters, database)
brewery_tab__gui = BreweryTabGUI(tab_control, brewery_parameters)
fermentation_tab_gui = FermentationTabGUI(tab_control, fermentation_parameters, database, dpi)
graph_tab_gui = GraphTabGUI(tab_control, database, dpi)
add_graph_tab_gui = AddGraphTabGUI(tab_control)

# Creating list with all tabs for loopings
tabs = [graph_tab_gui,
        add_graph_tab_gui,
        fermentation_tab_gui,
        recipe_tab_gui,
        brewery_tab__gui,
        ispindel_tab_gui,
        ]

# Adding tabs to tab bar
for tab in tabs:
    tab_control.add(tab, text=tab.name)

# Initial tab selection for resize of ispindel_tab_gui
# Selection of tab according to tabs list
tab_control.select(ispindel_tab_gui)
tab_control.select(0)

# Adding commands to GUI objects
tab_control.bind('<ButtonRelease-1>', add_graph_to_graph_tab_gui)

socket_thread = SocketThread(ispindel_tab_gui, fermentation_tab_gui)
root.mainloop()
