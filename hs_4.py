import socket
from tkinter import *
from tkinter import ttk
import threading
from ctypes import windll

from PIL import Image, ImageTk

"""THREADING"""


class App(threading.Thread):
    """A class to handle thread for socket"""

    def __init__(self, root):
        """Initialize class"""
        super().__init__()
        self.root = root
        self.daemon = True  # destroy when main thread is terminates
        self.start()
        self.message = {}

    def run(self):
        """Run socket loop"""
        while True:
            # Wait for a connection
            (connection, client_address) = sock.accept()

            label_ispindel_parameters_names.config(text='')
            label_ispindel_parameters_names.grid(row=0, column=0)
            label_ispindel_parameters_values.config(text='')
            label_ispindel_parameters_values.grid(row=0, column=0)
            label_ispindel_parameters_names.config(text='Data processing')
            label_ispindel_parameters_names.grid(row=0, column=0)

            message_string = ''
            parameters = ''
            values = ''

            try:
                while True:
                    data = connection.recv(200).decode("utf-8")

                    if data:
                        message_string += data
                    else:
                        message = eval(message_string)

                        label_ispindel_name.config(text=message['token'])
                        label_ispindel_name.place(relx=0.1, rely=0.71, anchor='center')
                        self.message = message
                        for key, value in message.items():
                            parameters += key.title() + '\n'
                            values += str(value) + '\n'

                        label_ispindel_parameters_names.config(text=parameters)
                        label_ispindel_parameters_names.grid(row=0, column=1)
                        label_ispindel_parameters_values.config(text=values)
                        label_ispindel_parameters_values.place(x=label_ispindel_parameters_names.winfo_width() + 20,
                                                               rely=0, anchor=NW)

                        break

            finally:
                # Clean up the connection
                connection.close()


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
    try:
        a = ((float(entry_gravity_point_1.get()) - float(entry_gravity_point_2.get())) /
             (calibration_point_1['Angle'] - calibration_point_2['Angle']))
        b = float(entry_gravity_point_1.get()) - a * calibration_point_1['Angle']
        label_generate_polynomial.config(text='y = ' + str(a) + 'x + ' + str(b))
    except KeyError:
        pass
    except ValueError:
        pass
    except ZeroDivisionError:
        pass

def resize_image(event):
    """Resize image when window size changed"""
    width, height = event.width, event.height
    caller = event.widget

    if caller == label_ispindel:
        image = image_ispindel_copy.resize((width, height))
        image_background_ispindel = ImageTk.PhotoImage(image)
        label_ispindel.config(image=image_background_ispindel)
        label_ispindel.image = image_background_ispindel  # avoid garbage collection, doesn't work without this line

    if caller == label_brewery:
        image = image_brewery_copy.resize((width, height))
        image_background_brewery = ImageTk.PhotoImage(image)
        label_brewery.config(image=image_background_brewery)
        label_brewery.image = image_background_brewery  # avoid garbage collection, doesn't work without this line


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


# Input
version = 4.01
icon = 'images/icon.ico'
image_ispindel = Image.open('images/iSpindel.bmp')
image_brewery = Image.open('images/Brewery.bmp')
title_str = 'Hajle Silesia Homebrewing System '
calibration_point_1 = {}
calibration_point_2 = {}

# Window setup
windll.shcore.SetProcessDpiAwareness(1)  # no blur of fonts - NOT WORKING
windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')

root = Tk()
root.minsize(image_ispindel.width, image_ispindel.height)
root.state('zoomed')  # maximize window
root.iconbitmap(icon)
root.title(title_str + str(version))

# Tab setup
style = ttk.Style()
style.configure('TNotebook.Tab', font=('None', '14'))

tab_control = ttk.Notebook(root)
tab_1 = Frame(tab_control)
tab_control.add(tab_1, text='iSpindel')
tab_2 = Frame(tab_control)
tab_control.add(tab_2, text='Brewery')
tab_control.pack(expand=1, fill='both')

# Image preparation
image_ispindel_copy = image_ispindel.copy()
image_background_ispindel = ImageTk.PhotoImage(image_ispindel)
image_brewery_copy = image_brewery.copy()
image_background_brewery = ImageTk.PhotoImage(image_brewery)

# Background image
label_ispindel = Label(tab_1, image=image_background_ispindel)
label_ispindel.bind('<Configure>', resize_image)  # widget changed its size
label_ispindel.place(relwidth=1, relheight=1)

label_brewery = Label(tab_2, image=image_background_brewery)
label_brewery.bind('<Configure>', resize_image)  # widget changed its size
label_brewery.place(relwidth=1, relheight=1)

# iSpindel labels
label_ispindel_name = Label(tab_1, font=(None, 14), bg='white')
label_ispindel_parameters_names = Label(tab_1, font=(None, 14), text='Waiting for data acquisition', bg='white',
                                        justify=LEFT)
label_ispindel_parameters_names.grid(row=0, column=0)
label_ispindel_parameters_values = Label(tab_1, font=(None, 14), bg='white', justify=LEFT)

# Frames
frame_entries_buttons = Frame(tab_1, bg='white')
frame_entries_buttons.place(relx=0.2, rely=0)

for i in range(7):
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

image_button = PhotoImage(file='images/but.png')
# image_button_copy = image_button.copy()
button_valve_1 = Button(tab_2, image=image_button, borderwidth=0, bg='white')
button_valve_1.place(relx=0.5, rely=0.5)

# Text
label_calibration_point_1 = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_calibration_point_1.grid(row=4, column=1, sticky=W+E)
label_calibration_point_2 = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_calibration_point_2.grid(row=5, column=1, sticky=W+E)
label_generate_polynomial = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_generate_polynomial.grid(row=6, column=1, sticky=W+E)

"""SOCKET"""
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (socket.gethostname(), 9501)
sock.bind(server_address)

# Listen for incoming connections (max 5 before refusing)
sock.listen(5)

# Create window
app = App(root)
root.mainloop()
