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

from PIL import Image, ImageTk
import pyodbc as db
from xml_list_config import *

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


def resize_image(event):
    """Resize image when window size changed"""
    global image_background_ispindel, image_background_brewery
    global image_button_toggle_switch_on, image_button_toggle_switch_off

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

    if caller == label_bk_cip:
        if not bk_cip:
            image = image_toggle_switch_off_copy.resize((width, height))
            image_button_toggle_switch_off = ImageTk.PhotoImage(image)
            label_bk_cip.config(image=image_button_toggle_switch_off)
            label_bk_cip.image = image_button_toggle_switch_off  # avoid garbage collection, doesn't work without this line
        else:
            image = image_toggle_switch_on_copy.resize((width, height))
            image_button_toggle_switch_on = ImageTk.PhotoImage(image)
            label_bk_cip.config(image=image_button_toggle_switch_on)
            label_bk_cip.image = image_button_toggle_switch_on  # avoid garbage collection, doesn't work without this line


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


def import_recipe():
    """Open dialog window to import XML recipe"""
    global xml_filepath, yos
    xml_filepath = filedialog.askopenfilename()

    recipe = element_tree.parse(xml_filepath).getroot()

    xml_dict = XmlDictConfig(recipe)
    mash_step = {}
    mash_steps = []
    mash_steps_texts = {'NAME': 'NAME', 'STEP_TIME': 'STEP_TIME', 'STEP_TEMP': 'STEP_TEMP'}
    hop = {}
    hops = []
    hops_texts = {'NAME': 'NAME', 'USE': 'USE', 'AMOUNT': 'AMOUNT', 'TIME': 'TIME'}
    misc = {}
    miscs = []
    miscs_texts = {'NAME': 'NAME', 'USE': 'USE', 'AMOUNT': 'AMOUNT', 'TIME': 'TIME'}
    fermentable = {}
    fermentables = []
    fermentables_texts = {'NAME': 'NAME', 'AMOUNT': 'AMOUNT'}
    parameters = OrderedDict()
    parameters_texts = {'NAME': 'NAME', 'VALUE': 'VALUE'}

    total_grains_weight = 0.0
    total_hops_weight = 0

    # RECIPE AND BATCH NUMBER
    label_recipe.config(text=xml_dict['RECIPE']['NAME'])
    label_recipe.grid(row=3, columnspan=6, sticky=NSEW)

    entry_batch_number.delete(0, END)
    entry_batch_number.insert(0, str(int(xml_dict['RECIPE']['NAME'].split()[0][1:])))
    entry_batch_number.config(fg='black')

    # MASH
    if 'MASH_STEPS' in xml_dict['RECIPE']['MASH']:
        for v in xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP']:
            # print(v)
            mash_step['NAME'] = v['NAME']
            mash_step['STEP_TIME'] = datetime.timedelta(minutes=int(round(float(v['STEP_TIME']), 0)))
            mash_step['STEP_TEMP'] = int(round(float(v['STEP_TEMP']), 0))
            mash_steps.append(copy.deepcopy(mash_step))  # deep copy to avoid binding each element of the list with variable

        for v in mash_steps:
            mash_steps_texts['NAME'] += '\n' + v['NAME']
            mash_steps_texts['STEP_TIME'] += '\n' + str(v['STEP_TIME'])
            mash_steps_texts['STEP_TEMP'] += '\n' + str(v['STEP_TEMP'])

    frame_mash_steps.grid(row=2, column=0, sticky=NSEW)
    label_mash_name.grid(row=0, columnspan=3)
    label_mash_steps_name.grid(row=1, column=0, sticky=W)
    label_mash_steps_step_time.grid(row=1, column=1, sticky=W)
    label_mash_steps_step_temp.grid(row=1, column=2, sticky=W)

    label_mash_name.config(text='Mash program: ' + xml_dict['RECIPE']['MASH']['NAME'])
    label_mash_steps_name.config(text=mash_steps_texts['NAME'])
    label_mash_steps_step_time.config(text=mash_steps_texts['STEP_TIME'])
    label_mash_steps_step_temp.config(text=mash_steps_texts['STEP_TEMP'])

    # HOPS
    if 'HOPS' in xml_dict['RECIPE']:

        for v in xml_dict['RECIPE']['HOPS']['HOP']:
            if v['USE'] == 'First Wort' or v['USE'] == 'Boil' or v['USE'] == 'Aroma':
                hop['NAME'] = v['NAME']
                hop['USE'] = v['USE']
                hop['AMOUNT'] = int(round(1e3 * float(v['AMOUNT']), 0))
                hop['TIME'] = datetime.timedelta(minutes=int(round(float(v['TIME']), 0)))
                total_hops_weight += hop['AMOUNT']
                hops.append(copy.deepcopy(hop))  # deep copy to avoid binding each element of the list with variable

        order = {'First Wort': 0, 'Boil': 1, 'Aroma': 2}
        hops = sorted(hops, key=lambda k: (order[k['USE']], -k['TIME']))

        for v in hops:
            hops_texts['NAME'] += '\n' + v['NAME']
            hops_texts['USE'] += '\n' + v['USE']
            hops_texts['AMOUNT'] += '\n' + str(v['AMOUNT'])
            hops_texts['TIME'] += '\n' + str(v['TIME'])

    frame_hops.grid(row=2, column=1, sticky=NSEW)
    label_hop_name.grid(row=0, columnspan=4)
    label_hops_name.grid(row=1, column=0, sticky=W)
    label_hops_use.grid(row=1, column=1, sticky=W)
    label_hops_amount.grid(row=1, column=2, sticky=W)
    label_hops_time.grid(row=1, column=3, sticky=W)

    label_hop_name.config(text='Hops, total: ' + str(total_hops_weight))
    label_hops_name.config(text=hops_texts['NAME'])
    label_hops_use.config(text=hops_texts['USE'])
    label_hops_amount.config(text=hops_texts['AMOUNT'])
    label_hops_time.config(text=hops_texts['TIME'])

    # MISC
    if 'MISCS' in xml_dict['RECIPE']:
        for v in xml_dict['RECIPE']['MISCS']['MISC']:
            misc['NAME'] = v['NAME']
            if v['USE']:
                misc['USE'] = v['USE']
            else:
                misc['USE'] = 'Sparge'
            misc['AMOUNT'] = round(1e3 * float(v['AMOUNT']), 2)
            misc['TIME'] = datetime.timedelta(minutes=int(round(float(v['TIME']), 0)))
            miscs.append(copy.deepcopy(misc))  # deep copy to avoid binding each element of the list with variable

            if v['NAME'] == "Baker's Dry Yeast" and not yos:
                label_yos.config(image=image_button_toggle_switch_on)
                yos = TRUE

        order = {'Mash': 0, 'Sparge': 1, 'Boil': 2}
        miscs = sorted(miscs, key=lambda k: (order[k['USE']], -k['TIME']))

        for v in miscs:
            miscs_texts['NAME'] += '\n' + v['NAME']
            miscs_texts['USE'] += '\n' + v['USE']
            miscs_texts['AMOUNT'] += '\n' + str(v['AMOUNT'])
            miscs_texts['TIME'] += '\n' + str(v['TIME'])

    frame_miscs.grid(row=1, column=0, sticky=NSEW)
    label_misc_name.grid(row=0, columnspan=4)
    label_miscs_name.grid(row=1, column=0, sticky=W)
    label_miscs_use.grid(row=1, column=1, sticky=W)
    label_miscs_amount.grid(row=1, column=2, sticky=W)
    label_miscs_time.grid(row=1, column=3, sticky=W)

    label_misc_name.config(text='Minerals & Boil additions')
    label_miscs_name.config(text=miscs_texts['NAME'])
    label_miscs_use.config(text=miscs_texts['USE'])
    label_miscs_amount.config(text=miscs_texts['AMOUNT'])
    label_miscs_time.config(text=miscs_texts['TIME'])

    # FERMENTABLES
    if 'FERMENTABLES' in xml_dict['RECIPE']:

        for v in xml_dict['RECIPE']['FERMENTABLES']['FERMENTABLE']:
            fermentable['NAME'] = v['NAME']
            fermentable['AMOUNT'] = round(float(v['AMOUNT']), 2)
            fermentables.append(copy.deepcopy(fermentable))  # deep copy to avoid binding each element of the list with variable

            if v['TYPE'] == 'Grain':
                total_grains_weight += fermentable['AMOUNT']

        total_grains_weight = round(total_grains_weight, 2)
        fermentables = sorted(fermentables, key=lambda k: (-k['AMOUNT']))

        for v in fermentables:
            fermentables_texts['NAME'] += '\n' + v['NAME']
            fermentables_texts['AMOUNT'] += '\n' + str(v['AMOUNT'])

    frame_fermentables.grid(row=1, column=1, sticky=NSEW)
    label_fermentable_name.grid(row=0, columnspan=2)
    label_fermentables_name.grid(row=1, column=0, sticky=W)
    label_fermentables_amount.grid(row=1, column=1, sticky=W)

    label_fermentable_name.config(text='Grains, total: ' + str(total_grains_weight))
    label_fermentables_name.config(text=fermentables_texts['NAME'])
    label_fermentables_amount.config(text=fermentables_texts['AMOUNT'])

    # PARAMETERS
    parameters['GRAIN_TEMP'] = round(float(xml_dict['RECIPE']['MASH']['GRAIN_TEMP']), 2)
    parameters['WATER_GRAIN_RATIO'] = round(float(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'][0]['WATER_GRAIN_RATIO'].split()[0].replace(',', '.')), 1)
    parameters['DISPLAY_INFUSE_AMT'] = round(float(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'][0]['DISPLAY_INFUSE_AMT'].split()[0]), 2)
    parameters['INFUSE_TEMP'] = round(float(xml_dict['RECIPE']['MASH']['MASH_STEPS']['MASH_STEP'][0]['INFUSE_TEMP'].split()[0]), 1)
    parameters['EQUIPMENT.LAUTER_DEADSPACE'] = round(float(xml_dict['RECIPE']['EQUIPMENT.LAUTER_DEADSPACE']), 2)

    parameters['SPARGE_VOLUME'] = round(float(xml_dict['RECIPE']['SPARGE_VOLUME'].split()[0]), 2)

    parameters['BOIL_SIZE'] = round(float(xml_dict['RECIPE']['BOIL_SIZE']), 2)
    parameters['PRE_BOIL_OG'] = round(float(xml_dict['RECIPE']['PRE_BOIL_OG'].split()[0]), 3)
    parameters['BOIL_TIME'] = datetime.timedelta(minutes=int(round(float(xml_dict['RECIPE']['BOIL_TIME']), 0)))

    parameters['EQUIPMENT.TRUB_CHILLER_LOSS'] = round(float(xml_dict['RECIPE']['EQUIPMENT.TRUB_CHILLER_LOSS']), 2)
    parameters['EQUIPMENT.COOLING_LOSS_PCT'] = round(float(xml_dict['RECIPE']['EQUIPMENT.COOLING_LOSS_PCT']), 2)
    parameters['EVAP_RATE'] = float(xml_dict['RECIPE']['EVAP_RATE'])
    parameters['POST_BOIL_VOLUME'] = round(parameters['BOIL_SIZE'] -\
                                     (parameters['EVAP_RATE'] / 100 * parameters['BOIL_SIZE'] *
                                      int(round(float(xml_dict['RECIPE']['BOIL_TIME']), 0)) / 60.0), 2)
    parameters['KNOCKOUT_VOLUME'] = round(parameters['POST_BOIL_VOLUME'] *
                                    (1 - parameters['EQUIPMENT.COOLING_LOSS_PCT'] / 100), 2)

    parameters['BATCH_SIZE'] = round(float(xml_dict['RECIPE']['BATCH_SIZE']), 2)
    parameters['PRIMARY_TEMP'] = int(round(float(xml_dict['RECIPE']['PRIMARY_TEMP']), 0))
    parameters['EST_OG'] = round(float(xml_dict['RECIPE']['EST_OG'].split()[0]), 3)
    parameters['IBU'] = round(float(xml_dict['RECIPE']['IBU'].split()[0]), 1)

    for k, v in parameters.items():
        parameters_texts['NAME'] += '\n' + k
        parameters_texts['VALUE'] += '\n' + str(v)

    frame_parameters.grid(row=1, column=2, rowspan=2, sticky=NSEW)
    label_parameter_name.grid(row=0, columnspan=2)
    label_parameters_name.grid(row=1, column=0, sticky=W)
    label_parameters_value.grid(row=1, column=1, sticky=W)

    label_parameter_name.config(text='Parameters, equipment: ' + xml_dict['RECIPE']['EQUIPMENT.NAME'])
    label_parameters_name.config(text=parameters_texts['NAME'])
    label_parameters_value.config(text=parameters_texts['VALUE'])


def user_setup(event):
    """Turn on / off CIP program for BK / MLT"""
    caller = event.widget
    global bk_cip, mlt_cip, bk_rinse, mlt_rinse, yos

    if caller == label_bk_cip:
        if not bk_cip:
            label_bk_cip.config(image=image_button_toggle_switch_on)
            label_bk_rinse.config(image=image_button_toggle_switch_on)
            bk_cip = TRUE
            bk_rinse = TRUE
        else:
            label_bk_cip.config(image=image_button_toggle_switch_off)
            bk_cip = FALSE
    elif caller == label_mlt_cip:
        if not mlt_cip:
            label_mlt_cip.config(image=image_button_toggle_switch_on)
            label_mlt_rinse.config(image=image_button_toggle_switch_on)
            mlt_cip = TRUE
            mlt_rinse = TRUE
        else:
            label_mlt_cip.config(image=image_button_toggle_switch_off)
            mlt_cip = FALSE
    elif caller == label_bk_rinse:
        if not bk_rinse:
            label_bk_rinse.config(image=image_button_toggle_switch_on)
            bk_rinse = TRUE
        else:
            label_bk_rinse.config(image=image_button_toggle_switch_off)
            label_bk_cip.config(image=image_button_toggle_switch_off)
            bk_rinse = FALSE
            bk_cip = FALSE
    elif caller == label_mlt_rinse:
        if not mlt_rinse:
            label_mlt_rinse.config(image=image_button_toggle_switch_on)
            mlt_rinse = TRUE
        else:
            label_mlt_rinse.config(image=image_button_toggle_switch_off)
            label_mlt_cip.config(image=image_button_toggle_switch_off)
            mlt_rinse = FALSE
            mlt_cip = FALSE
    elif caller == label_yos:
        if not yos:
            label_yos.config(image=image_button_toggle_switch_on)
            yos = TRUE
        else:
            label_yos.config(image=image_button_toggle_switch_off)
            yos = FALSE


# Input
version = 4.01
icon = 'images/icon.ico'
image_ispindel = Image.open('images/iSpindel.bmp')
image_brewery = Image.open('images/Brewery.bmp')
title_str = 'Hajle Silesia Homebrewing System '
calibration_point_1 = {}
calibration_point_2 = {}
a = 0.0
b = 0.0
xml_filepath = ''
bk_cip = FALSE
mlt_cip = FALSE
bk_rinse = FALSE
mlt_rinse = FALSE
yos = FALSE

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

tab_ispindel = Frame(tab_control)
tab_brewery = Frame(tab_control)
tab_recipe = Frame(tab_control)
tab_graph = Frame(tab_control)

tab_control.add(tab_recipe, text='Recipe')
tab_control.add(tab_brewery, text='Brewery')
tab_control.add(tab_ispindel, text='iSpindel')
tab_control.add(tab_graph, text='Graph')

tab_control.pack(expand=1, fill='both')

# Image preparation
image_ispindel_copy = image_ispindel.copy()
image_background_ispindel = ImageTk.PhotoImage(image_ispindel)
image_brewery_copy = image_brewery.copy()
image_background_brewery = ImageTk.PhotoImage(image_brewery)

# Background image
label_ispindel = Label(tab_ispindel, image=image_background_ispindel)
label_ispindel.bind('<Configure>', resize_image)  # widget changed its size
label_ispindel.place(relwidth=1, relheight=1)

label_brewery = Label(tab_brewery, image=image_background_brewery)
label_brewery.bind('<Configure>', resize_image)  # widget changed its size
label_brewery.place(relwidth=1, relheight=1)

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

# Recipe tab
frame_user_settings = Frame(tab_recipe)
frame_user_settings.grid(row=0, columnspan=3, sticky=W+E)

for i in range(6):
    frame_user_settings.columnconfigure(i, weight=1, uniform='column')

for i in range(4):
    frame_user_settings.rowconfigure(i, weight=1, uniform='row')

frame_user_settings.rowconfigure(0, weight=1, uniform='row')

button_import_recipe = Button(frame_user_settings, text='Import recipe', font=(None, 14), command=import_recipe)
button_import_recipe.grid(row=1, column=0)

image_toggle_switch_on = Image.open('images/toggle_switch_on_c.png')
image_toggle_switch_off = Image.open('images/toggle_switch_off_c.png')

image_toggle_switch_on_copy = image_toggle_switch_on.copy()
image_button_toggle_switch_on = ImageTk.PhotoImage(image=image_toggle_switch_on)

image_toggle_switch_off_copy = image_toggle_switch_off.copy()
image_button_toggle_switch_off = ImageTk.PhotoImage(image=image_toggle_switch_off)

label_bk_cip_setting = Label(frame_user_settings, font=(None, 14), text='BK CIP')
label_bk_cip_setting.grid(row=0, column=5)

label_mlt_cip_setting = Label(frame_user_settings, font=(None, 14), text='MLT CIP')
label_mlt_cip_setting.grid(row=0, column=3)

label_bk_rinse_setting = Label(frame_user_settings, font=(None, 14), text='BK rinse')
label_bk_rinse_setting.grid(row=0, column=4)

label_mlt_rinse_setting = Label(frame_user_settings, font=(None, 14), text='MLT rinse')
label_mlt_rinse_setting.grid(row=0, column=2)

label_yos_setting = Label(frame_user_settings, font=(None, 14), text='YOS')
label_yos_setting.grid(row=0, column=1)

label_bk_cip = Label(frame_user_settings, image=image_button_toggle_switch_off, borderwidth=0)
label_bk_cip.bind('<Button-1>', user_setup)
label_bk_cip.grid(row=1, column=5)

label_mlt_cip = Label(frame_user_settings, image=image_button_toggle_switch_off, borderwidth=0)
label_mlt_cip.bind('<Button-1>', user_setup)
label_mlt_cip.grid(row=1, column=3)

label_bk_rinse = Label(frame_user_settings, image=image_button_toggle_switch_off, borderwidth=0)
label_bk_rinse.bind('<Button-1>', user_setup)
label_bk_rinse.grid(row=1, column=4)

label_mlt_rinse = Label(frame_user_settings, image=image_button_toggle_switch_off, borderwidth=0)
label_mlt_rinse.bind('<Button-1>', user_setup)
label_mlt_rinse.grid(row=1, column=2)

label_yos = Label(frame_user_settings, image=image_button_toggle_switch_off, borderwidth=0)
label_yos.bind('<Button-1>', user_setup)
label_yos.grid(row=1, column=1)

label_recipe = Label(frame_user_settings, font=(None, 20, 'bold'))

image_button = PhotoImage(file='images/but.png')
# image_button_copy = image_button.copy()
button_valve_1 = Button(tab_brewery, image=image_button, borderwidth=0, bg='white')
button_valve_1.place(relx=0.5, rely=0.5)

# Text
label_calibration_point_1 = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_calibration_point_1.grid(row=4, column=1, sticky=W+E)
label_calibration_point_2 = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_calibration_point_2.grid(row=5, column=1, sticky=W+E)
label_generate_polynomial = Label(frame_entries_buttons, font=(None, 14), bg='white', anchor=W)
label_generate_polynomial.grid(row=6, column=1, sticky=W+E)

# Text XML
frame_mash_steps = Frame(tab_recipe, borderwidth=4, relief='solid')
for i in range(3):
    frame_mash_steps.columnconfigure(i, weight=1)

label_mash_name = Label(frame_mash_steps, font=(None, 20, 'bold'), text='')
label_mash_steps_name = Label(frame_mash_steps, font=(None, 14), text='', justify=LEFT)
label_mash_steps_step_time = Label(frame_mash_steps, font=(None, 14), text='', justify=LEFT)
label_mash_steps_step_temp = Label(frame_mash_steps, font=(None, 14), text='', justify=LEFT)

for i in range(2):
    ttk.Separator(frame_mash_steps, orient=VERTICAL).grid(row=1, column=i, padx=20, sticky=N+S+E)

frame_hops = Frame(tab_recipe, borderwidth=4, relief='solid')
for i in range(4):
    frame_hops.columnconfigure(i, weight=1)

label_hop_name = Label(frame_hops, font=(None, 20, 'bold'), text='')
label_hops_name = Label(frame_hops, font=(None, 14), text='', justify=LEFT)
label_hops_use = Label(frame_hops, font=(None, 14), text='', justify=LEFT)
label_hops_amount = Label(frame_hops, font=(None, 14), text='', justify=LEFT)
label_hops_time = Label(frame_hops, font=(None, 14), text='', justify=LEFT)

for i in range(3):
    ttk.Separator(frame_hops, orient=VERTICAL).grid(row=1, column=i, padx=20, sticky=N+S+E)

frame_miscs = Frame(tab_recipe, borderwidth=4, relief='solid')
for i in range(4):
    frame_miscs.columnconfigure(i, weight=1)

label_misc_name = Label(frame_miscs, font=(None, 20, 'bold'), text='')
label_miscs_name = Label(frame_miscs, font=(None, 14), text='', justify=LEFT)
label_miscs_use = Label(frame_miscs, font=(None, 14), text='', justify=LEFT)
label_miscs_amount = Label(frame_miscs, font=(None, 14), text='', justify=LEFT)
label_miscs_time = Label(frame_miscs, font=(None, 14), text='', justify=LEFT)

for i in range(3):
    ttk.Separator(frame_miscs, orient=VERTICAL).grid(row=1, column=i, padx=20, sticky=N+S+E)

frame_fermentables = Frame(tab_recipe, borderwidth=4, relief='solid')
for i in range(2):
    frame_fermentables.columnconfigure(i, weight=1)

label_fermentable_name = Label(frame_fermentables, font=(None, 20, 'bold'), text='')
label_fermentables_name = Label(frame_fermentables, font=(None, 14), text='', justify=LEFT)
label_fermentables_amount = Label(frame_fermentables, font=(None, 14), text='', justify=LEFT)

for i in range(1):
    ttk.Separator(frame_fermentables, orient=VERTICAL).grid(row=1, column=i, padx=20, sticky=N+S+E)

frame_parameters = Frame(tab_recipe, borderwidth=4, relief='solid')
for i in range(2):
    frame_parameters.columnconfigure(i, weight=1)

label_parameter_name = Label(frame_parameters, font=(None, 20, 'bold'), text='')
label_parameters_name = Label(frame_parameters, font=(None, 14), text='', justify=LEFT)
label_parameters_value = Label(frame_parameters, font=(None, 14), text='', justify=LEFT)

for i in range(1):
    ttk.Separator(frame_parameters, orient=VERTICAL).grid(row=1, column=i, padx=20, sticky=N+S+E)

for i in range(3):
    tab_recipe.columnconfigure(i, weight=1, uniform='column')
tab_recipe.rowconfigure(1, weight=1)
tab_recipe.rowconfigure(2, weight=1)

"""SOCKET"""
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (socket.gethostname(), 9501)
sock.bind(server_address)

# Listen for incoming connections (max 5 before refusing)
sock.listen(5)

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
