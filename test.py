from tkinter import *
from PIL import Image, ImageTk


def resize(event):
    global c_img, img
    width, height = event.width, event.height
    w_scale = width / img.width
    h_scale = width / img.height

    image = img_c.resize((width, height))
    c_img = ImageTk.PhotoImage(image)
    can.itemconfig(c_back, image=c_img)

    can.coords(c_line, 20 * w_scale, 20 * h_scale, 200 * w_scale, 200 * h_scale)

root = Tk()
root.state('zoomed')
can = Canvas(root)

img = Image.open('images/ispindel2.bmp')
img_c = img.copy()
c_img = ImageTk.PhotoImage(image=img)

c_back = can.create_image(0, 0, anchor=N + W, image=c_img)
c_line = can.create_line(20, 20, 200, 200, width=2)
can.place(relwidth=1, relheight=1)
can.bind('<Configure>', resize)

root.mainloop()