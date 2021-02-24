import sys
import cv2
import threading
import tkinter as tk
import tkinter.ttk as ttk
from queue import Queue
from PIL import Image
from PIL import ImageTk


class App(tk.Frame):
    def __init__(self, parent, title):
        tk.Frame.__init__(self, parent)
        self.is_running = False
        self.thread = None
        self.queue = Queue()
        self.photo = ImageTk.PhotoImage(Image.new("RGB", (800, 600), "white"))
        parent.wm_withdraw()
        parent.wm_title(title)
        self.create_ui()
        self.grid(sticky=tk.NSEW)
        self.bind('<<MessageGenerated>>', self.on_next_frame)
        parent.wm_protocol("WM_DELETE_WINDOW", self.on_destroy)
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
        parent.wm_deiconify()

    def create_ui(self):
        self.button_frame = ttk.Frame(self)
        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.RIGHT)
        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.RIGHT)
        self.view = ttk.Label(self, image=self.photo)
        self.view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

    def on_destroy(self):
        self.stop()
        self.after(20)
        if self.thread is not None:
            self.thread.join(0.2)
        self.winfo_toplevel().destroy()

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.is_running = False

    def videoLoop(self, mirror=False):
        No='rtsp://admin:123456a@192.168.0.103:554/live/ch00_1'
        cap = cv2.VideoCapture(No)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        while self.is_running:
            ret, to_draw = cap.read()
            if mirror is True:
                to_draw = to_draw[:,::-1]
            image = cv2.cvtColor(to_draw, cv2.COLOR_BGR2RGB)
            self.queue.put(image)
            self.event_generate('<<MessageGenerated>>')

    def on_next_frame(self, eventargs):
        if not self.queue.empty():
            image = self.queue.get()
            image = Image.fromarray(image)
            self.photo = ImageTk.PhotoImage(image)
            self.view.configure(image=self.photo)


def main(args):
    root = tk.Tk()
    app = App(root, "OpenCV Image Viewer")
    root.mainloop()

if __name__ == '__main__':
    sys.exit(main(sys.argv))