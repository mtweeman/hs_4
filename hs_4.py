import socket
from tkinter import *
import threading
import os

from PIL import Image, ImageTk
import pyodbc as db

"""TKINTER"""


def calibrate_ispindel(event):
    """Print and save calibration point into Access database"""
    caller = event.widget

    try:
        if caller == button_calibration_point_1:
            calibration_point_1['Gravity'] = float(entry_gravity_point_1.get())
            calibration_point_1['Angle'] = app.message['angle']
            label_calibration_point_1.config(text=calibration_point_1)

        if caller == button_calibration_point_2:
            calibration_point_2['Gravity'] = float(entry_gravity_point_2.get())
            calibration_point_2['Angle'] = app.message['angle']
            label_calibration_point_2.config(text=calibration_point_2)
    except KeyError:
        pass
    except ValueError:
        pass


def generate_polynomial(event):
    """Calculate, print and save polynomial into Access database"""
    global a, b

    try:
        a = ((float(entry_gravity_point_1.get()) - float(entry_gravity_point_2.get())) /
             (calibration_point_1['Angle'] - calibration_point_2['Angle']))
        b = float(entry_gravity_point_1.get()) - a * calibration_point_1['Angle']
        label_generate_polynomial.config(text='y = ' + str(a) + 'x + ' + str(b))
        print(a, b)
    except KeyError:
        pass
    except ValueError:
        pass
    except ZeroDivisionError:
        pass


def entry_click(event):
    """Hide entry default text when clicked (or focused)"""
    caller = event.widget

    if caller == entry_batch_number and entry_batch_number.get() == 'Batch number':
        event.widget.delete(0, END)
        entry_batch_number.config(fg='black')

    if caller == entry_temperature_offset and entry_temperature_offset.get() == 'Temperature offset':
        event.widget.delete(0, END)
        entry_temperature_offset.config(fg='black')

    if caller == entry_gravity_point_1 and entry_gravity_point_1.get() == 'Gravity point 1':
        event.widget.delete(0, END)
        entry_gravity_point_1.config(fg='black')

    if caller == entry_gravity_point_2 and entry_gravity_point_2.get() == 'Gravity point 2':
        event.widget.delete(0, END)
        entry_gravity_point_2.config(fg='black')


def entry_unclick(event):
    """Hide entry default text when clicked or focused"""
    caller = event.widget

    if caller == entry_batch_number and not entry_batch_number.get():
        entry_batch_number.insert(0, 'Batch number')
        entry_batch_number.config(fg='#c5c5c5')

    if caller == entry_temperature_offset and not entry_temperature_offset.get():
        entry_temperature_offset.insert(0, 'Temperature offset')
        entry_temperature_offset.config(fg='#c5c5c5')

    if caller == entry_gravity_point_1 and not entry_gravity_point_1.get():
        entry_gravity_point_1.insert(0, 'Gravity point 1')
        entry_gravity_point_1.config(fg='#c5c5c5')

    if caller == entry_gravity_point_2 and not entry_gravity_point_2.get():
        entry_gravity_point_2.insert(0, 'Gravity point 2')
        entry_gravity_point_2.config(fg='#c5c5c5')


def confirm_settings(event):
    """Confirm and save settings to Access database"""
    global query

    # Establish connection with local database and create cursor object
    db_connection = db.connect(connection_string, autocommit=True)
    cursor = db_connection.cursor()

    # Fill table with new values
    query = ("""INSERT INTO Fermentation_settings""" +
             """(batch_number,""" +
             """temperature_offset,""" +
             """gravity_1,""" +
             """gravity_2,""" +
             """angle_1,""" +
             """angle_2,""" +
             """a,""" +
             """b) VALUES """ +
             """(""" +
             str(entry_batch_number.get()) + """,""" +
             str(entry_temperature_offset.get()) + """,""" +
             str(calibration_point_1['Gravity']) + """,""" +
             str(calibration_point_2['Gravity']) + """,""" +
             str(calibration_point_1['Angle']) + """,""" +
             str(calibration_point_2['Angle']) + """,""" +
             str(a) + """,""" +
             str(b) +
             """);""")

    db_connection.execute(query)

    # Close cursor and connection with database
    cursor.close()
    db_connection.close()

# Input
calibration_point_1 = {}
calibration_point_2 = {}
a = 0.0
b = 0.0


# Tab setup

# iSpindel labels
label_ispindel_name = Label(tab_ispindel, font=(None, 14), bg='white')
label_ispindel_parameters_names = Label(tab_ispindel, font=(None, 14), text='Waiting for data acquisition', bg='white',
                                        justify=LEFT)
label_ispindel_parameters_names.grid(row=0, column=0)
label_ispindel_parameters_values = Label(tab_ispindel, font=(None, 14), bg='white', justify=LEFT)

# Frames
frame_entries_buttons = Frame(tab_ispindel, bg='white')
frame_entries_buttons.place(relx=0.2, rely=0)

for i in range(8):
    frame_entries_buttons.rowconfigure(i, weight=1, uniform='row')

# Entries
entry_batch_number = Entry(frame_entries_buttons, font=(None, 14), bg='white', fg='#c5c5c5')
entry_batch_number.insert(END, 'Batch number')
entry_batch_number.bind('<FocusIn>', entry_click)
entry_batch_number.bind('<FocusOut>', entry_unclick)
entry_batch_number.grid(row=0, column=0, sticky=W+E)

entry_temperature_offset = Entry(frame_entries_buttons, font=(None, 14), bg='white', fg='#c5c5c5')
entry_temperature_offset.insert(END, 'Temperature offset')
entry_temperature_offset.bind('<FocusIn>', entry_click)
entry_temperature_offset.bind('<FocusOut>', entry_unclick)
entry_temperature_offset.grid(row=1, column=0, sticky=W+E)

entry_gravity_point_1 = Entry(frame_entries_buttons, font=(None, 14), bg='white', fg='black')
entry_gravity_point_1.insert(END, '1.000')
entry_gravity_point_1.bind('<FocusIn>', entry_click)
entry_gravity_point_1.bind('<FocusOut>', entry_unclick)
entry_gravity_point_1.grid(row=2, column=0, sticky=W+E)

entry_gravity_point_2 = Entry(frame_entries_buttons, font=(None, 14), bg='white', fg='#c5c5c5')
entry_gravity_point_2.insert(END, 'Gravity point 2')
entry_gravity_point_2.bind('<FocusIn>', entry_click)
entry_gravity_point_2.bind('<FocusOut>', entry_unclick)
entry_gravity_point_2.grid(row=3, column=0, sticky=W+E)

# Buttons setup
# iSpindel tab
button_calibration_point_1 = Button(frame_entries_buttons, text='Calibrate point 1', font=(None, 14),
                                    anchor=W)
button_calibration_point_1.bind('<Button-1>', calibrate_ispindel)
button_calibration_point_1.grid(row=4, column=0, sticky=W+E)

button_calibration_point_2 = Button(frame_entries_buttons, text='Calibrate point 2', font=(None, 14),
                                    anchor=W)
button_calibration_point_2.bind('<Button-1>', calibrate_ispindel)
button_calibration_point_2.grid(row=5, column=0, sticky=W+E)

button_generate_polynomial = Button(frame_entries_buttons, text='Generate polynomial', font=(None, 14),
                                    anchor=W)
button_generate_polynomial.bind('<Button-1>', generate_polynomial)
button_generate_polynomial.grid(row=6, column=0, sticky=W+E)

button_confirm_settings = Button(frame_entries_buttons, text='Confirm settings', font=(None, 14),
                                 anchor=W)
button_confirm_settings.bind('<Button-1>', confirm_settings)
button_confirm_settings.grid(row=7, column=0, sticky=W+E)

# Text
label_calibration_point_1 = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_calibration_point_1.grid(row=4, column=1, sticky=W+E)
label_calibration_point_2 = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_calibration_point_2.grid(row=5, column=1, sticky=W+E)
label_generate_polynomial = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_generate_polynomial.grid(row=6, column=1, sticky=W+E)

"""DATABASE"""
# Database setup
database_path = os.getcwd() + r"/hajle_silesia_db.accdb"
connection_string = ("Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
                     "DBQ=" + database_path + ";")

# Establish connection with local database and create cursor object
db_connection = db.connect(connection_string, autocommit=True)
cursor = db_connection.cursor()

# Prepare query for table creation
query = ("""CREATE TABLE Fermentation_settings""" +
         """(batch_number short PRIMARY KEY NOT NULL,""" +
         """temperature_offset DOUBLE NOT NULL, """ +
         """gravity_1 DOUBLE NOT NULL,""" +
         """gravity_2 DOUBLE NOT NULL,""" +
         """angle_1 DOUBLE NOT NULL,""" +
         """angle_2 DOUBLE NOT NULL,""" +
         """a DOUBLE NOT NULL,""" +
         """b DOUBLE NOT NULL);""")

# Check existence / create table
if not cursor.tables(table='Fermentation_settings', tableType='TABLE').fetchone():
    db_connection.execute(query)

# Close cursor and connection with database
cursor.close()
db_connection.close()

# Create window
app = App(root)
root.mainloop()
