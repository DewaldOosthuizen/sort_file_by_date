import os
import os.path
import shutil
import time
from datetime import datetime
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

# This script opens a gui application.
# The application allows you to select a directory.s
# Once a directory has been selected the directory path will be
# displayed to the user along with a sort bytton next to it.
# If the user clicks on the sort button, all files within the selected
# folder will be sorted by date into sub folders. 
# NOTE: This will move the file from its orinal location, into a folder
# inside the original location called 'soreted'. Inside the sorted folder
# you will find folders with dates as the folder name. All files created
# on that date will be moved into that directory.

## VARIABALES ##
dir_to_sort = ""

## FUNCTIONS ##

#
#  name: ask_dir
#  @param self
#  @return void
#
# this method asks the user to select a directory
def ask_dir():
	global dir_to_sort
	dir_to_sort = filedialog.askdirectory()

	if Path(str(dir_to_sort)).exists() and str(dir_to_sort) is not "":
		print(dir_to_sort)
		dir_text['text'] = str(dir_to_sort)
		start_sort.grid(row=1, column=0)

		
#
#  name: sort_files
#  @param self
#  @return void
#
# this method sorts all the files in the selected directory by date
def sort_files():
	# check if the selected path exists and is a directory
	global dir_to_sort
	if Path(str(dir_to_sort)).exists() is False or Path(str(dir_to_sort)).is_dir() is False or str(dir_to_sort) is "":
		messagebox.showinfo("Whoops!", "Please select a valid directory")
		raise # stop running the method
	
	txt.insert(END, "\n" + "Directory " + str(dir_to_sort) + " is valid..")
	
	#get all files in a directory
	txt.insert(END, "\n" + "Checking directory " + dir_to_sort + " for files..")
	lis = os.listdir(str(dir_to_sort))
	lis.sort()
	
	txt.insert(END, "\n" + "Files in directory: " + str(lis))
	
	# check that the directory is not empty
	if len(lis) <= 0:
		messagebox.showinfo("Whoops!", "The selected directory has no files in it")
		raise # stop running the method
	
	# start moving the files into folders
	for x in lis:
		txt.insert(END, "\n" + "Working with " + dir_to_sort + "/" + x)
		
		if Path(dir_to_sort + "/" + x).is_file() is False:
			txt.insert(END, "\n" + x + " is a directory, skipping")
			continue
		
		if Path(dir_to_sort + "/" + x).exists() is False or Path(
				dir_to_sort + "/" + x).is_file() is False:
			txt.insert(END, "\n" + x + " is not a valid file")
			continue

		txt.insert(END, "\n" + x + " is a valid file")
		try:
			txt.insert(END, "\n" + "getting data for " + x)
			datestring = time.ctime(os.path.getmtime(dir_to_sort + "/" + x))
			dt = datetime.strptime(datestring, '%a %b %d %H:%M:%S %Y')

			destinationDir = dir_to_sort + "/sorted/" + str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day)
			txt.insert(END, "\n" + "Determined destination to move file to: " + destinationDir)

			if not os.path.exists(destinationDir):
				os.makedirs(destinationDir)
				txt.insert(END, ("\n" +"created folder: %s" % destinationDir))
			txt.insert(END, "\n" +"Moving file...")
			shutil.move(dir_to_sort + "/" + x, destinationDir)

			txt.insert(END, "\n" + x + " moved successfully")
		except FileNotFoundError as e:
			txt.insert(END, ("\nFailed to move " + x + ", reason: " + str(e)))
		
	txt.insert(END, ("\n::  Done  ::"))

## MAIN ##
win = Tk()
win.title("File Date sorter")

# Button to choose directory
dir_select = Button(
	win,
	text="Choose Directory",
	command=ask_dir,
	bg="green",
	width=15
)
dir_select.grid(row=0, column=0)

# Quit button to quit the application
quit = Button(
	win,
	text="QUIT",
	bg="red",
	command=win.destroy,
	width=15
)
quit.grid(row=0, column=1)

# Button to start the sorting process
start_sort = Button(
	win,
	text="Start Sorting",
	command=sort_files,
	bg="teal",
	width=15
)
start_sort.grid(row=1, column=0)
start_sort.grid_forget()

# create a label with the slected directory path
dir_text = Label(win, text=str(dir_to_sort))
dir_text.grid(row=1, column=1)	

# create a new frame for textarea
frame = Frame(win)
frame.grid(row=2, columnspan=2)

# create a Text widget
txt = Text(frame, borderwidth=3, relief="sunken")
txt.config(font=("consolas", 12), undo=True, wrap='word')
txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

# create a Scrollbar and associate it with txt
scrollb = Scrollbar(frame, command=txt.yview)
scrollb.grid(row=0, column=1, sticky='nsew')
txt['yscrollcommand'] = scrollb.set
txt.insert(END, "To get started, choose a directory where the files are you would like to sort")     

win.mainloop()
