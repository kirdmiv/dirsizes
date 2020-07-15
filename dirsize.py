import os
import time
from tkinter import *  # you should install it


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
frame = Frame(root)
frame.pack()
changed = True
sizes = {}

gu = Button(root, text="..", width=30, command=goUp)
gu.pack()

while True:
    if changed:
        all = os.listdir()
        frame.destroy()
        frame = Frame(root)
        frame.pack()
        for item in all:
            print(item)
            name = str(item)
            # name.set(str(item))
            # Button(frame, width=30, bg="white", text=name, command = lambda: goDown(this.text)).pack()
            labelText = " ".join([name, humanReadableSize(getSize(name))])
            b = Button(frame, width=30, bg="white", text=labelText)
            b.config(command=lambda x=name: goDown(x))
            b.pack()
        changed = False

    root.update()
    time.sleep(0.1)
