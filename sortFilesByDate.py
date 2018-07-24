import os
import os.path
import shutil
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

# This script opens a gui application.
# The application allows you to select a directory.
# Once a directory has been selected the directory path will be
# displayed to the user along with a sort button next to it.
# If the user clicks on the sort button, all files within the selected
# folder will be sorted by date into sub folders.
# NOTE: This will move the file from its orinal location, into a folder
# inside the original location called 'sorted'. Inside the sorted folder
# you will find folders with dates as the folder name. All files created
# on that date will be moved into that directory.

## VARIABALES ##
dir_to_sort = ""

#
#  name: ask_dir
#  @param self
#  @return void
#
# this method asks the user to select a directory
def ask_dir():
    dir_to_sort = filedialog.askdirectory()

    if Path(str(dir_to_sort)).exists() and dir_to_sort is not "":
        print(dir_to_sort)
        dir_text["text"] = "Selected directory: " + str(dir_to_sort)

#
#  name: sort_files
#  @param self
#  @return void
#
# this method sorts all the files in the selected directory by date
def sort_files():
    lis = os.listdir(dir_to_sort)
    lis.sort()
    print(dir_to_sort)
    print(str(lis))
    for x in lis:
        if Path(dir_to_sort + "/" + x).exists() is False or Path(
                dir_to_sort + "/" + x).is_file() is False:
            continue

        try:
            print(("created folder: %s" % time.ctime(os.path.getctime(x))))
            datestring = time.ctime(os.path.getmtime(x))
            dt = datetime.strptime(datestring, '%a %b %d %H:%M:%S %Y')

            destinationDir = str(dir_to_sort) + "/sorted/"
            str(dt.month) + '-' + str(dt.day) + '-' + str(dt.year)

            print(destinationDir)
            if not os.path.exists(destinationDir):
                os.makedirs(destinationDir)
            shutil.move(x, destinationDir)
        except FileNotFoundError as e:
            print(("Failed to move " + x + ", reason: " + str(e)))


# main application start
win = tk.Tk()
win.title("File Date Sorter")

## CREATE UI COMPONENTS ##
# Intro text
intro = tk.Label(win, text='Please select a directory. I will then sort all your files in that '
                                 'directory by date. \nI will do this by creating folders with the date as '
                                 'the folder name and will then move files with the same date into the '
                                 'corresponding folder').grid(row=0, column=0)

tk.Label(win, text='').grid(row=1, column=0) # force a blank line TODO: Find a better way to do this

# Button to choose directory
dir_select = tk.Button(
    win,
    text="Choose Directory",
    command=ask_dir,
    bg="green"
).grid(row=2, column=0)

dir_text = tk.Label(win, text="Selected directory: ").grid(row=3, column=0)
# Button to start the sorting process
start_sort = tk.Button(
    win,
    text="Start Sorting",
    command=sort_files,
    bg="teal"
).grid(row=4, column=0)

tk.Label(win, text='').grid(row=5, column=0) # force a blank line TODO: Find a better way to do this
tk.Label(win, text='').grid(row=6, column=0) # force a blank line TODO: Find a better way to do this

# Quit button to quit the application
quit = tk.Button(
    win,
    text="QUIT",
    bg="red",
    command=win.destroy
).grid(row=7, column=1)


print(dir_text)
win.mainloop()
