# Standard libraries
from tkinter import *
import csv

# Imported libraries
from PIL import Image, ImageTk

# My libraries
from sparklines_gui import SparklinesGUI
from requester_socket_thread import RequesterSocketThread


class FermentationTabGUI(Frame):
    """A class for Fermentation tab creation"""
    def __init__(self, tab_control, fermentation_parameters, database, dpi, mail):
        super().__init__(tab_control)
        self.name = 'Fermentation'
        self.fermentation_parameters = fermentation_parameters
        self.database = database
        self.dpi = dpi
        self.mail = mail
        self.w_scale = 1
        self.h_scale = 1

        # Images for labels
        self.img_fermentation = Image.open('images/ferm6.bmp')
        self.img_toggle_on = Image.open('images/toggle_on.png')
        self.img_toggle_off = Image.open('images/toggle_off.png')
        self.img_button_on = Image.open('images/button_on.png')
        self.img_button_off = Image.open('images/button_off.png')

        self.img_toggle_on = self.img_toggle_on.resize((60, 38))
        self.img_toggle_off = self.img_toggle_off.resize((60, 38))
        self.img_button_on = self.img_button_on.resize((40, 40))
        self.img_button_off = self.img_button_off.resize((40, 40))

        self.img_fermentation_copy = self.img_fermentation.copy()
        self.img_toggle_on_copy = self.img_toggle_on.copy()
        self.img_toggle_off_copy = self.img_toggle_off.copy()
        self.img_button_on_copy = self.img_button_on.copy()
        self.img_button_off_copy = self.img_button_off.copy()

        self.img_c_fermentation = ImageTk.PhotoImage(image=self.img_fermentation)
        self.img_c_toggle_on = ImageTk.PhotoImage(image=self.img_toggle_on)
        self.img_c_toggle_off = ImageTk.PhotoImage(image=self.img_toggle_off)
        self.img_c_button_on = ImageTk.PhotoImage(image=self.img_button_on)
        self.img_c_button_off = ImageTk.PhotoImage(image=self.img_button_off)

        # CATIA coordinates for GUI objects
        filename = 'data/fermentation_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.fermentation_coords = {}

            for row in reader:
                if row[0] == 'rect':
                    self.fermentation_rect = (int(row[1]), int(row[2]))
                else:
                    self.fermentation_coords[row[0]] = (int(row[1]), int(row[2]))

        # Names of GUI objects in the tab
        self.c_fermentation = Canvas(self)
        self.f_status = Frame(self, bg='#555555')

        # f_status
        self.l_statuses = {}
        self.l_signs = {}

        for i, pair in enumerate(self.fermentation_parameters.parameters.items()):
            if pair[0] in self.fermentation_parameters.fermentation_parameters:
                # name column
                Label(self.f_status, fg='white', bg='#555555', font=(None, 14),
                      text=pair[0].replace('temperature_', 't ').upper()).grid(row=i, column=0, padx=20, sticky=W)

                # value column
                if pair[0] == 'microcontroller' or pair[0] == 'sensors':
                    self.l_statuses[pair[0]] = \
                        Label(self.f_status, fg='red', bg='#555555', font=(None, 14), text=pair[1].upper())
                elif pair[0] == 'temperature_set':
                    self.l_signs['-'] = \
                        Label(self.f_status, fg='white', bg='blue', font=('Consolas', 14), text=' - ')
                    self.l_statuses[pair[0]] = \
                        Label(self.f_status, fg='white', bg='#555555', font=(None, 14), text='%.2f' % pair[1])
                    self.l_signs['+'] = \
                        Label(self.f_status, fg='white', bg='red', font=('Consolas', 14), text=' + ')
                else:
                    self.l_statuses[pair[0]] = \
                        Label(self.f_status, fg='white', bg='#555555', font=(None, 14), text='%.2f' % pair[1])

        # c_fermentation
        self.c_items = {}  # buttons and toggles
        self.f_frames = {}
        self.l_labels = {}
        self.f_sparklines = {}
        self.c_background = self.c_fermentation.create_image(0, 0, anchor=N + W, image=self.img_c_fermentation)

        for k, v in self.fermentation_coords.items():
            if 'fv' in k or 'master' in k:
                # Toggles
                self.c_items[k] = self.c_fermentation.create_image(
                    int(round(self.w_scale * self.img_fermentation.width * (v[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.h_scale * self.img_fermentation.height * (v[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_toggle_off)

                # Frames associated with fermentation vessels
                if 'fv' in k:
                    self.f_frames[k] = Frame(self)
                    self.l_labels[k] = Label(
                        self.f_frames[k], fg='white', bg='#555555', font=(None, 14), text=k.replace('_', ' ').upper())
                    self.f_sparklines[k] = SparklinesGUI(self.f_frames[k], self.database, self.dpi)
            else:
                # Buttons
                self.c_items[k] = self.c_fermentation.create_image(
                    int(round(self.w_scale * self.img_fermentation.width * (v[0] / self.fermentation_rect[0]), 0)),
                    int(round(self.h_scale * self.img_fermentation.height * (v[1] / self.fermentation_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_button_off)

        # Adding GUI objects to the grid
        self.c_fermentation.place(relwidth=1, relheight=1)
        self.f_status.place(relx=0.01, rely=0.087, anchor=N + W)

        # f_status
        for i, k in enumerate(self.l_statuses):
            if k == 'temperature_set':
                self.l_signs['-'].grid(row=i, column=1, sticky=E)
                self.l_statuses[k].grid(row=i, column=2, padx=20)
                self.l_signs['+'].grid(row=i, column=3, sticky=W)
            else:
                self.l_statuses[k].grid(row=i, column=1, padx=20, columnspan=3)

        # c_fermentation
        for k, v in self.fermentation_coords.items():
            if 'fv' in k:
                self.f_frames[k].place(relx=v[0] / self.fermentation_rect[0],
                                       rely=(v[1] + self.img_toggle_on.height) / self.fermentation_rect[1],
                                       relwidth=0.1,
                                       relheight=0.2,
                                       anchor=N)
                self.l_labels[k].grid(row=0, column=0, sticky=NSEW)
                self.f_sparklines[k].grid(row=1, column=0, sticky=NSEW)

                # Checking fermentation vessel for log = True or master = True
                # if log = True - update sparklines (so far only empty figure) and labels
                # if master = True - update labels
                result = self.database.get_fermentation_settings_batch_number_batch_name(k)
                if result:
                    self.f_sparklines[k].update_sparklines(result[0])
                    self.l_labels[k].config(text=k.replace('_', ' ').upper() + '\n' + result[1])
                else:
                    result = self.database.get_fermentation_settings_batch_name(k)
                    if result:
                        self.l_labels[k].config(text=k.replace('_', ' ').upper() + '\n' + result)

        # Adding commands to GUI objects
        self.c_fermentation.bind('<Configure>', self.resize_image)

        # f_status
        # for k in self.l_signs:
        #     self.l_signs[k].bind('<Button-1>', self.change_temperature_manually)

        # c_fermentation
        for k in self.fermentation_coords:
            self.c_fermentation.tag_bind(self.c_items[k], '<Button-1>', lambda event, key=k: self.toggle_switch(key))

        # Setting rows and columns properties
        # f_status
        self.f_status.columnconfigure(0, weight=3, uniform='column')
        self.f_status.columnconfigure(1, weight=1, uniform='column')
        self.f_status.columnconfigure(2, weight=1, uniform='column')
        self.f_status.columnconfigure(3, weight=1, uniform='column')

        # c_fermentation
        for k in self.f_frames:
            self.f_frames[k].columnconfigure(0, weight=1)
            self.f_frames[k].rowconfigure(1, weight=1)

        # Binding with slave socket
        # self.l_status has to be initialized first
        self.fermentation_socket_thread = RequesterSocketThread(self, self.fermentation_parameters.parameters)

    def resize_image(self, event):
        # Getting scale
        width, height = event.width, event.height

        self.w_scale = width / self.img_fermentation.width
        self.h_scale = height / self.img_fermentation.height

        # Resizing images
        # img_brewery
        image = self.img_fermentation_copy.resize((width, height))
        self.img_c_fermentation = ImageTk.PhotoImage(image)

        # img_toggle_on
        image = self.img_toggle_on_copy.resize(
            (int(round(self.w_scale * self.img_toggle_on.width, 0)),
             int(round(self.h_scale * self.img_toggle_on.height, 0))))
        self.img_c_toggle_on = ImageTk.PhotoImage(image)

        # img_toggle_off
        image = self.img_toggle_off_copy.resize(
            (int(round(self.w_scale * self.img_toggle_off.width, 0)),
             int(round(self.h_scale * self.img_toggle_off.height, 0))))
        self.img_c_toggle_off = ImageTk.PhotoImage(image)

        # img_button_on
        image = self.img_button_on_copy.resize(
            (int(round(self.w_scale * self.img_button_on.width, 0)),
             int(round(self.h_scale * self.img_button_on.height, 0))))
        self.img_c_button_on = ImageTk.PhotoImage(image)

        # img_button_off
        image = self.img_button_off_copy.resize(
            (int(round(self.w_scale * self.img_button_off.width, 0)),
             int(round(self.h_scale * self.img_button_off.height, 0))))
        self.img_c_button_off = ImageTk.PhotoImage(image)

        # Updating canvas
        self.c_fermentation.itemconfig(self.c_background, image=self.img_c_fermentation)
        self.update_toggles_and_buttons()

        # Updating coordinates of GUI objects
        for k, v in self.fermentation_coords.items():
            self.c_fermentation.coords(self.c_items[k],
                                       int(round(self.w_scale * self.img_fermentation.width *
                                                 (v[0] / self.fermentation_rect[0]), 0)),
                                       int(round(self.h_scale * self.img_fermentation.height *
                                                 (v[1] / self.fermentation_rect[1]), 0)))

    def update_toggles_and_buttons(self):
        for k in self.fermentation_parameters.parameters:
            if 'fv' in k or 'master' in k:
                if self.fermentation_parameters.parameters[k]:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_toggle_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_toggle_off)
            elif k == 'freezer':
                if self.fermentation_parameters.parameters[k]:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_button_on)
                else:
                    self.c_fermentation.itemconfig(self.c_items[k], image=self.img_c_button_off)

    def toggle_switch(self, key):
        self.fermentation_parameters.verify_parameters(key)
        self.update_toggles_and_buttons()

        self.c_fermentation.update_idletasks()

        # Updating database
        if 'fv' in key:
            self.database.execute_fermentation_settings_log(key, self.fermentation_parameters.parameters[key])
        elif 'master' in key:
            self.database.execute_fermentation_settings_master(key.replace('master', 'fv'),
                                                               self.fermentation_parameters.parameters[key])

        # Updating data on screen
        if 'fv' in key:
            if self.fermentation_parameters.parameters[key]:
                result = self.database.get_fermentation_settings_batch_number_batch_name(key)
                if result:
                    self.f_sparklines[key].update_sparklines(result[0])
                    if not self.fermentation_parameters.parameters[key.replace('fv', 'master')]:
                        self.l_labels[key].config(text=key.replace('_', ' ').upper() + '\n' + result[1])
            else:
                self.f_sparklines[key].clear_sparklines()
                if not self.fermentation_parameters.parameters[key.replace('fv', 'master')]:
                    self.l_labels[key].config(text=key.replace('_', ' ').upper())
        elif 'master' in key:
            if self.fermentation_parameters.parameters[key]:
                if not self.fermentation_parameters.parameters[key.replace('master', 'fv')]:
                    result = self.database.get_fermentation_settings_batch_number_batch_name(
                        key.replace('master', 'fv'), False)
                    if result:
                        self.l_labels[key.replace('master', 'fv')].config(text=key.replace('master_', 'fv ').upper() +
                                                                               '\n' + result[1])
            else:
                if not self.fermentation_parameters.parameters[key.replace('master', 'fv')]:
                    self.l_labels[key.replace('master', 'fv')].config(text=key.replace('master_', 'fv ').upper())

    def ispindel_socket_parameters_update(self, socket_message):
        # Checking if log = True for fermentation_vessel OR master
        result = self.database.get_fermentation_settings(socket_message['name'], True)
        if not result:
            result = self.database.get_fermentation_settings(socket_message['name'], False)

        if result:
            # Calculating gravity basing on polynomial and temperature with offset
            socket_message['gravity'] = socket_message['angle'] * result[2] + result[3]
            socket_message['temperature'] = socket_message['temperature'] + result[4]

            # Updating database and sparklines if log = True
            del socket_message['name']

            if result[5]:
                self.database.execute_fermentation(result[1], socket_message)
                self.f_sparklines[result[0]].update_sparklines()

            # Updating data on screen
            self.l_labels[result[0]].config(text=result[0].replace('_', ' ').upper() + '\n' +
                                                 result[6] + '\n' +
                                                 'T: ' + '%.1f' % socket_message['temperature'] + '\n' +
                                                 'SG: ' + '%.3f' % socket_message['gravity'])

            # Setting fermentation notification
            # fermentation start when 1 SG point dropped
            start_notification = self.database.get_fermentation_settings_start(result[1])

            if result[7] - socket_message['gravity'] >= 0.001 and not start_notification:
                self.database.execute_fermentation_settings_start(result[1])
                self.mail.fermentation_start_notification(result[1], result[6])

    def slave_socket_parameters_update(self, socket_message):
        # Extracting parameters
        # parameters controlled by server are not overwritten
        for k, v in socket_message.items():
            if '_set' not in k and '_offset' not in k and self.fermentation_parameters.parameters[k] != v:
                self.fermentation_parameters.parameters[k] = v

        # Printing socket data on the screen
        for k, v in socket_message.items():
            if '_set' not in k and '_offset' not in k and k in self.l_statuses:
                if k == 'microcontroller' or k == 'sensors':
                    self.l_statuses[k].config(text=str(v).upper())
                    if v == 'online':
                        self.l_statuses[k].config(fg='#34C85A')
                    else:
                        self.l_statuses[k].config(fg='red')
                else:
                    self.l_statuses[k].config(text='%.2f' % v)

    def change_temperature_manually(self, event):
        # Updating parameters
        for v in self.l_signs.values():
            if v == event.widget:
                if '+' in v.cget('text'):
                    self.fermentation_parameters.parameters['temperature_set'] += 0.1
                else:
                    self.fermentation_parameters.parameters['temperature_set'] -= 0.1
                break

        # Printing data on the screen
        self.l_statuses['temperature_set'].config(text='%.2f' %
                                                       self.fermentation_parameters.parameters['temperature_set'])

        # Sending update to slave socket
        self.fermentation_socket_thread.transmit('temperature_set=' +
                                                 str(self.fermentation_parameters.parameters['temperature_set']))
