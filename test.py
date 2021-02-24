from tkinter import *

a = 1.234
b = 'online'
print(type(a))
print(type(b))

root = Tk()
f = Frame(root, borderwidth=4, relief=SOLID)
l1 = Label(f, text='%.2f' % a, borderwidth=4, relief=SOLID)
l2 = Label(f, text='testasdasdasd', borderwidth=4, relief=SOLID)
l1.config(text=b)

f.place(x=0, y=0, width=500, height=500)
l1.grid(row=0, column=0)
l2.grid(row=1, column=0)

# f.columnconfigure(0, weight=1)

root.mainloop()