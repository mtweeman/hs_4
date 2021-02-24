# Standard libraries
import threading
import time
import datetime

# Imported libraries
from PIL import Image, ImageTk
import cv2

# My libraries


class Camera(threading.Thread):
    def __init__(self, queue, label, parameter, key):
        threading.Thread.__init__(self, daemon=True)
        self.queue = queue
        self.label = label
        self.parameter = parameter
        self.k = key

        self.start()

    def run(self):
        self.cam = cv2.VideoCapture('rtsp://admin:123456a@192.168.0.103:554/live/ch00_1')
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # print('run')
        if self.cam.isOpened():
            while self.parameter[self.k]:
                ret, frame = self.cam.read()
                # print(ret)
                if ret:
                    # Preparing picture
                    # flip = cv2.flip(frame, 1)
                    flip = frame
                    rot = cv2.rotate(flip, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    # rot = cv2.rotate(rot, cv2.ROTATE_90_CLOCKWISE)
                    img_cv2 = cv2.cvtColor(rot, cv2.COLOR_BGR2RGBA)
                    self.img_cam = Image.fromarray(img_cv2)

                    self.queue.put(self.img_cam.copy())
                    self.label.event_generate('<<MessageGenerated>>')
        else:
            self.cam.release()
            self.queue.put('inufo')
            self.label.event_generate('<<MessageGenerated>>')
