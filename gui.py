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
from recipe_parameters import RecipeParameters
from brewery_parameters import BreweryParameters
from ispindel_parameters import ISpindelParameters
from socket_thread import SocketThread
from database import Database

# Input
version = 4.01
icon = 'images/icon.ico'
image_brewery = Image.open('images/test7.bmp')
title_str = 'Hajle Silesia Homebrewing System '

recipe_parameters = RecipeParameters()
brewery_parameters = BreweryParameters()
ispindel_parameters = ISpindelParameters()
database = Database()

# Window setup
windll.shcore.SetProcessDpiAwareness(1)  # no blur of fonts - NOT WORKING
windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')

root = Tk()
root.minsize(image_brewery.width, image_brewery.height)
root.state('zoomed')  # maximize window
root.iconbitmap(icon)
root.title(title_str + str(version))

# Tabs setup
tab_control = ttk.Notebook(root)
tab_control.pack(fill='both', expand=1)

ispindel_tab_gui = ISpindelTabGUI(tab_control, ispindel_parameters, database)
recipe_tab_gui = RecipeTabGUI(tab_control, recipe_parameters)
brewery_tab__gui = BreweryTabGUI(tab_control, brewery_parameters)

tabs = [ispindel_tab_gui,
        recipe_tab_gui,
        brewery_tab__gui,
        ]

for tab in tabs:
    tab_control.add(tab, text=tab.name)

socket_thread = SocketThread(ispindel_tab_gui)
root.mainloop()
