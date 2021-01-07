# Standard libraries
from tkinter import *

# Imported libraries
from PIL import Image, ImageTk
import cv2

# My libraries


class Camera(Frame):
    def __init__(self, camera_frame):
        super().__init__(camera_frame)
        self.width_zoom = 450
        self.height_zoom = 800
        self.width_normal = 99
        self.height_normal = 176
        self.width = self.width_normal
        self.height = self.height_normal
        self.zoom = False
        self.cam = cv2.VideoCapture('rtsp://admin:123456a@192.168.0.103:554/live/ch00_1')

        # Names of GUI objects in the tab
        self.l_cam = Label(self)

        # Adding GUI objects to the grid
        # self.l_cam.place(relwidth=1, relheight=1)
        self.l_cam.pack(expand=1, fill=BOTH)

        # Adding commands to GUI objects
        self.l_cam.bind('<Button-1>', self.resize_image)

        self.show_frame()

    def resize_image(self, event):
        if self.zoom:
            self.width = self.width_normal
            self.height = self.height_normal
            self.zoom = False
        else:
            self.width = self.width_zoom
            self.height = self.height_zoom
            self.zoom = True

    def show_frame(self):
        ret, frame = self.cam.read()
        if ret:
            # flip = cv2.flip(frame, 1)
            flip = frame
            rot = cv2.rotate(flip, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # rot = cv2.rotate(rot, cv2.ROTATE_90_CLOCKWISE)
            img_cv2 = cv2.cvtColor(rot, cv2.COLOR_BGR2RGBA)
            self.img_cam = Image.fromarray(img_cv2)
            self.img_cam = self.img_cam.resize((self.width, self.height))
            self.img_l_cam = ImageTk.PhotoImage(image=self.img_cam)
            self.l_cam.img_l_cam = self.img_l_cam
            self.l_cam.config(image=self.img_l_cam)
        self.l_cam.after(40, self.show_frame)

    def remove_camera(self):
        cv2.destroyAllWindows()
