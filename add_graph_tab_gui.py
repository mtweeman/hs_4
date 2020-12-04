# Standard libraries
from tkinter import *
from tkinter import ttk

# Imported libraries


# My libraries


class AddGraphTabGUI(Button):
    """A class for 'AddGraph' tab creation"""
    def __init__(self, tab_control1):
        super().__init__(tab_control1)
        self.name = '+'
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=(None, 14))
