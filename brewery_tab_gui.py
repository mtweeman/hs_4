# Standard libraries
from tkinter import *
import csv
from queue import Queue
import threading
import datetime

# Imported libraries
from PIL import Image, ImageTk

# My libraries
# from camera_thread import Camera
from camera_thread_test import Camera


class BreweryTabGUI(Frame):
    """A class for Brewery tab creation"""

    def __init__(self, tab_control, brewery_parameters):
        super().__init__(tab_control)
        self.name = 'Brewery'
        self.brewery_parameters = brewery_parameters
        self.w_scale = 1
        self.h_scale = 1
        self.queue = Queue()

        # Images for labels
        self.img_brewery = Image.open('images/test7.bmp')
        self.img_button_on = Image.open('images/button_on.png')
        self.img_button_off = Image.open('images/button_off.png')

        self.img_brewery_copy = self.img_brewery.copy()
        self.img_button_on_copy = self.img_button_on.copy()
        self.img_button_off_copy = self.img_button_off.copy()

        self.img_c_brewery = ImageTk.PhotoImage(image=self.img_brewery)
        self.img_c_button_on = ImageTk.PhotoImage(image=self.img_button_on)
        self.img_c_button_off = ImageTk.PhotoImage(image=self.img_button_off)

        # CATIA coordinates for GUI objects
        filename = 'data/brewery_coords.csv'

        with open(filename) as f_obj:
            reader = csv.reader(f_obj)
            next(reader)

            self.brewery_coords = {}

            for row in reader:
                if row[0] == 'rect':
                    self.brewery_rect = (int(row[1]), int(row[2]))
                else:
                    self.brewery_coords[row[0]] = (int(row[1]), int(row[2]))

        # Names of GUI objects in the tab
        self.c_brewery = Canvas(self)

        # c_brewery
        self.c_items = {}  # buttons
        self.f_cams = {}  # frames for cams
        self.l_cams = {}  # labels for cams
        self.i_cams = {}  # sizes for cams
        self.b_cams = {}  # zoom for cams
        self.cams = {}
        self.img_cams = {}
        self.img_l_cams = {}
        self.c_background = self.c_brewery.create_image(0, 0, anchor=N + W, image=self.img_c_brewery)

        for k, v in self.brewery_coords.items():
            if '_cam' in k:
                # frames and labels for cams
                self.f_cams[k] = Frame(self)
                self.l_cams[k] = Label(self.f_cams[k], font=(None, 14), text='NA')
                # print(id(self.l_cams[k]))
                self.b_cams[k] = False
            elif '_size' in k:
                pass
            else:
                # buttons
                self.c_items[k] = self.c_brewery.create_image(
                    int(round(self.w_scale * self.img_brewery.width * (v[0] / self.brewery_rect[0]), 0)),
                    int(round(self.h_scale * self.img_brewery.height * (v[1] / self.brewery_rect[1]), 0)),
                    anchor=CENTER, image=self.img_c_button_off)

        for k, v in self.brewery_parameters.parameters.items():
            if '_sightglass' in k:
                self.i_cams[k + '_size'] = (self.brewery_coords[k + '_cam'][0] / self.brewery_rect[0],
                                            self.brewery_coords[k + '_cam'][1] / self.brewery_rect[1],
                                            2 * abs(self.brewery_coords[k + '_cam'][0] -
                                                    self.brewery_coords[k + '_size'][0]) / self.brewery_rect[0],
                                            2 * abs(self.brewery_coords[k + '_cam'][1] -
                                                    self.brewery_coords[k + '_size'][1]) / self.brewery_rect[1],
                                            )

        # Adding GUI objects to the grid
        self.c_brewery.place(relwidth=1, relheight=1)

        # Adding commands to GUI objects
        self.c_brewery.bind('<Configure>', self.resize_image)

        for k in self.brewery_coords:
            if '_cam' in k:
                self.l_cams[k].bind('<<MessageGenerated>>', lambda event, key=k: self.video_refresh(key))
                self.l_cams[k].bind('<Button-1>', lambda event, key=k: self.video_zoom(key))
            elif '_size' in k:
                pass
            else:
                self.c_brewery.tag_bind(self.c_items[k], '<Button-1>', lambda event, key=k: self.button_switch(key))

    def video_zoom(self, key):
        if self.b_cams[key]:
            self.f_cams[key].place_forget()
            self.f_cams[key].place(relx=self.i_cams[key.replace('_cam', '_size')][0],
                                   rely=self.i_cams[key.replace('_cam', '_size')][1],
                                   relwidth=self.i_cams[key.replace('_cam', '_size')][2],
                                   relheight=self.i_cams[key.replace('_cam', '_size')][3],
                                   anchor=CENTER)
            self.b_cams[key] = False
        else:
            self.f_cams[key].place_forget()
            self.f_cams[key].place(relx=self.i_cams[key.replace('_cam', '_size')][0],
                                   rely=self.i_cams[key.replace('_cam', '_size')][1],
                                   width=self.image.width,
                                   height=self.image.height,
                                   anchor=CENTER)
            self.b_cams[key] = True

    def video_refresh(self, key):
        # print('refresh')
        if not self.queue.empty():
            self.image = self.queue.get()
            # print(self.image)
            if not isinstance(self.image, str):
                self.img_cams[key] = self.image.resize((self.f_cams[key].winfo_width(),
                                                                self.f_cams[key].winfo_height()))
                self.img_l_cams[key] = ImageTk.PhotoImage(image=self.img_cams[key])
                self.l_cams[key].config(image=self.img_l_cams[key])
            else:
                self.l_cams[key].config(text=self.image)


    def resize_image(self, event):
        # Getting scale
        width, height = event.width, event.height

        self.w_scale = width / self.img_brewery.width
        self.h_scale = height / self.img_brewery.height

        # Resizing images
        # img_brewery
        image = self.img_brewery_copy.resize((width, height))
        self.img_c_brewery = ImageTk.PhotoImage(image)

        # img_button_on
        image = self.img_button_on_copy.resize((int(round(self.w_scale * self.img_button_on.width, 0)),
                                                int(round(self.h_scale * self.img_button_on.height, 0))))
        self.img_c_button_on = ImageTk.PhotoImage(image)

        # img_button_off
        image = self.img_button_off_copy.resize((int(round(self.w_scale * self.img_button_off.width, 0)),
                                                 int(round(self.h_scale * self.img_button_off.height, 0))))
        self.img_c_button_off = ImageTk.PhotoImage(image)

        # Updating canvas
        self.c_brewery.itemconfig(self.c_background, image=self.img_c_brewery)
        self.update_buttons()

        # Updating coordinates of GUI objects
        for k, v in self.brewery_coords.items():
            if '_cam' not in k and '_size' not in k:
                self.c_brewery.coords(self.c_items[k],
                                      int(round(self.w_scale * self.img_brewery.width *
                                                (v[0] / self.brewery_rect[0]), 0)),
                                      int(round(self.h_scale * self.img_brewery.height *
                                                (v[1] / self.brewery_rect[1]), 0)))

    def button_switch(self, key):
        self.brewery_parameters.verify_parameters(key)
        self.update_buttons()
        self.execute_action(key)

    def update_buttons(self):
        for k in self.c_items:
            if self.brewery_parameters.parameters[k]:
                self.c_brewery.itemconfig(self.c_items[k], image=self.img_c_button_on)
            else:
                self.c_brewery.itemconfig(self.c_items[k], image=self.img_c_button_off)

    def execute_action(self, key):
        if '_sightglass' in key:
            if self.brewery_parameters.parameters[key]:
                self.l_cams[key + '_cam'].pack(fill=BOTH, expand=1)
                self.f_cams[key + '_cam'].place(relx=self.i_cams[key + '_size'][0],
                                                rely=self.i_cams[key + '_size'][1],
                                                relwidth=self.i_cams[key + '_size'][2],
                                                relheight=self.i_cams[key + '_size'][3],
                                                anchor=CENTER)
                print(datetime.datetime.now())
                self.cams[key + '_cam'] = Camera(self.queue, self.l_cams[key + '_cam'],
                                                 self.brewery_parameters.parameters,
                                                 key,
                                                 )
                print(self.cams[key + '_cam'])
                print(datetime.datetime.now())
            else:
                self.f_cams[key + '_cam'].place_forget()
                self.cams[key + '_cam'] = None
