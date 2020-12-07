from tkinter import *
from tkinter import ttk

root = Tk()

tab_control = ttk.Notebook(root)
tab_control.pack(fill='both', expand=1)

style = ttk.Style()
style.theme_create('tab_bar_theme', parent='classic', settings={'TNotebook': {'configure': {'background': '#888888'}},
                                                                'TNotebook.Tab': {'configure': {'background': '#555555',
                                                                                                'foreground': 'white',
                                                                                                'padding': [10, 10]},
                                                                                  'label': {'side': ''},
                                                                                  'map': {'background': [
                                                                                      ('selected', '#ffffff')],
                                                                                      'foreground': [
                                                                                          ('selected', 'black')]}}})
style.theme_use('tab_bar_theme')

for i in range(6):
    tab_control.add(Frame(), text='Tab' + str(i))

f_user_settings = Frame(tab_control)
tab_control.add(f_user_settings)
cb_fv = ttk.Combobox(f_user_settings, font=(None, 14), values=['0', '1'])
cb_fv.pack()

root.mainloop()
