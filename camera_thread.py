# Standard libraries
from tkinter import *
import threading

# Imported libraries
from PIL import Image, ImageTk
import cv2

# My libraries


class Camera(Frame, threading.Thread):
    def __init__(self, camera_frame, camera_size):
        Frame.__init__(self, camera_frame, )
        threading.Thread.__init__(self, daemon=True)
        self.camera_frame = camera_frame
        self.camera_size = camera_size
        self.width_zoom = None
        self.height_zoom = None
        self.zoom = False
        self.cam = cv2.VideoCapture('rtsp://admin:123456a@192.168.0.103:554/live/ch00_1')

        # Names of GUI objects in the tab
        self.l_cam = Label(self.camera_frame)

        # Adding GUI objects to the grid
        self.l_cam.pack(expand=1, fill=BOTH)

        # Adding commands to GUI objects
        self.l_cam.bind('<Button-1>', self.resize_image)

        self.show_frame()

    def resize_image(self, event):
        if self.zoom:
            self.camera_frame.place_forget()
            self.camera_frame.place(relx=self.camera_size[0],
                                    rely=self.camera_size[1],
                                    relwidth=self.camera_size[2],
                                    relheight=self.camera_size[3],
                                    anchor=CENTER)
            self.zoom = False
        else:
            self.camera_frame.place_forget()
            self.camera_frame.place(relx=self.camera_size[0],
                                    rely=self.camera_size[1],
                                    width=self.width_zoom,
                                    height=self.height_zoom,
                                    anchor=CENTER)
            self.zoom = True

    def show_frame(self):
        ret, frame = self.cam.read()
        if ret:
            # Preparing picture
            # flip = cv2.flip(frame, 1)
            flip = frame
            rot = cv2.rotate(flip, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # rot = cv2.rotate(rot, cv2.ROTATE_90_CLOCKWISE)
            img_cv2 = cv2.cvtColor(rot, cv2.COLOR_BGR2RGBA)
            self.img_cam = Image.fromarray(img_cv2)

            # Setting normal picture size if not set
            if not self.width_zoom and not self.height_zoom:
                self.width_zoom = self.img_cam.width
                self.height_zoom = self.img_cam.height

            self.img_cam = self.img_cam.resize((self.camera_frame.winfo_width(), self.camera_frame.winfo_height()))
            self.img_l_cam = ImageTk.PhotoImage(image=self.img_cam)
            self.l_cam.img_l_cam = self.img_l_cam
            self.l_cam.config(image=self.img_l_cam)

        self.l_cam.after(10, self.show_frame)
