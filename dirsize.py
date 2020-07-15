import os
import time
from tkinter import *


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


def goUp():
    global changed
    # os.chdir(os.getcwd() + os.path.sep + "..")
    os.chdir(os.path.join(os.getcwd(), ".."))
    changed = True


def goDown(dirName):
    global changed
    # os.chdir(os.getcwd() + os.path.sep + dirName)
    os.chdir(os.path.join(os.getcwd(), dirName))
    changed = True


def getDirSize(dirName):
    global sizes
    size = 0
    for dirpath, dirnames, filenames in os.walk(os.path.join(os.getcwd(), dirName)):
        # print("Calc size of", dirpath)
        dirsize = 0
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            if not os.path.islink(filepath):
                filesize = getSize(filepath, True)
                # print("Size of", filepath, filesize)
                size += filesize
                dirsize += filesize
                sizes[filepath] = filesize
        sizes[dirpath] = dirsize
    return size


def getSize(itemName, isFile=False):
    global sizes
    if sizes.get(itemName) != None:
        return sizes[itemName]
    if '.' in itemName or isFile:
        try:
            return os.path.getsize(os.path.join(os.getcwd(), itemName))
        except OSError:
            return 0
    else:
        return getDirSize(itemName)


def humanReadableSize(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


root = Tk()
frame = VerticalScrolledFrame(root)
frame.pack()
changed = True
sizes = {}

while True:
    if changed:
        all_files = os.listdir()
        frame.destroy()
        frame = VerticalScrolledFrame(root)
        frame.pack()
        gu = Button(frame.interior, text="..", width=30, bg="white", command=goUp)
        gu.pack()
        for item in all_files:
            print(item)
            name = str(item)
            # name.set(str(item))
            # Button(frame, width=30, bg="white", text=name, command = lambda: goDown(this.text)).pack()
            labelText = " ".join([name, humanReadableSize(getSize(name))])
            b = Button(frame.interior, width=30, bg="white", text=labelText)
            b.config(command=lambda x=name: goDown(x))
            b.pack()
        changed = False

    root.update()
    time.sleep(0.1)
