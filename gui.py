# Standard libraries
import socket
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import threading
from ctypes import windll
import os
import xml.etree.ElementTree as element_tree
import copy
import datetime
from _collections import OrderedDict
import smtplib
from email.message import EmailMessage

# Imported libraries
from PIL import Image, ImageTk
import pyodbc as db

# My libraries
from xml_list_config import *
from recipe_tab_gui import RecipeTabGUI
from brewery_tab_gui import BreweryTabGUI
from ispindel_tab_gui import iSpindelTabGUI
from recipe_parameters import RecipeParameters
from brewery_parameters import BreweryParameters
from ispindel_parameters import iSpindelParameters

# Input
version = 4.01
icon = 'images/icon.ico'
image_brewery = Image.open('images/test7.bmp')
title_str = 'Hajle Silesia Homebrewing System '

recipe_parameters = RecipeParameters()
brewery_parameters = BreweryParameters()
ispindel_parameters = iSpindelParameters()

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

tabs = [iSpindelTabGUI(tab_control, ispindel_parameters),
        RecipeTabGUI(tab_control, recipe_parameters),
        BreweryTabGUI(tab_control, brewery_parameters),
        ]

for tab in tabs:
    tab_control.add(tab, text=tab.name)

root.mainloop()
