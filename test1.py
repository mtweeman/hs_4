from tkinter import *
from test import thr
from queue import Queue

def gui(event):
    if not queue.empty():
        queue.get()

def err(event):
    if not queue.empty():
        queue.get()

def watek(label, queue):
    thread = thr(label, queue)
    print('watek')

root = Tk()
queue = Queue()
l = Label(root, text='NA')
b = Button(root, text='przycisk')
l.grid(row=0, column=0)
b.grid(row=1, column=0)
l.bind('<<GUIUpdate>>', gui)
l.bind('<<GUIError>>', err)
b.bind('<Button-1>', lambda event, label=l: watek(label, queue))

root.mainloop()