# Creates two identical panels.  Zooming in on the right panel will show
# a rectangle in the first panel, denoting the zoomed region.
import numpy as np
import sys
import os
import webbrowser
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import AfmDisplay
import CustomToolbar
import UpdatingRect
import backgroundremoval
import nanowire_detector as ND


def clear_canvas():
    """Deletes previous canvases"""

    if len(toolbars) > 0:
        toolbars[-1].destroy()

    if len(canvases) > 0:
        canvases[-1].get_tk_widget().delete("all")
        canvases[-1].get_tk_widget().destroy()

    return

def get_lims():
	master = tk.Tk()
	
	msg = tk.Label(master, text="Enter limits").grid(row=0)
	
	
	tk.Label(master, text="Min X [ nm ]").grid(row=1, column=0)
	tk.Label(master, text="Max X [ nm ]").grid(row=1, column=2)
	tk.Label(master, text="Min Y [ nm ]").grid(row=2, column=0)
	tk.Label(master, text="Max Y [ nm ]").grid(row=2, column=2)

	min_x = tk.Entry(master)
	min_y = tk.Entry(master)
	max_y = tk.Entry(master)
	max_x = tk.Entry(master)
	
	min_x.insert(10,"0")
	min_y.insert(10,"0")
	max_x.insert(10,"500")
	max_y.insert(10,"500")

	min_x.grid(row=1, column=1)
	min_y.grid(row=2, column=1)
	max_x.grid(row=1, column=3)
	max_y.grid(row=2, column=3)
	

	button = tk.Button(master, text="Dismiss", command=master.destroy).grid(row=3)
	
	#return


def upload_file():
    """ Upload the chosen file and plot the nanowire image onto the canvas"""
    filename = filedialog.askopenfilename()
    file_data = np.genfromtxt(filename)
    
    # Changing the range of data to 0 ...
    file_data= file_data - np.min(file_data)
    file_data= file_data*(255.0)/np.max(file_data)

    get_lims()
    
    afmimg, hull_points, wire_with_line, profile = ND.top_level(np.uint8(file_data))
    

    global md
    md = AfmDisplay.AfmDisplay(d=file_data)
    plot_data(md)

    return


def plot_data(md):

    xmax, ymax = np.shape(md.data)
    Z = md(0, xmax, 0, ymax)
    clear_canvas()

    plt.rcParams.update(params)

    fig1, (ax1, ax2) = plt.subplots(1, 2)

    #ax1.matshow(Z, origin='lower', extent=(0, xmax, 0, ymax), cmap=color_code)
    ax1.matshow(Z, origin='lower', extent=(0, 500, 0, 500), cmap=color_code, aspect='auto')
    ax2.matshow(Z, origin='lower', extent=(0, xmax, 0, ymax), cmap=color_code, aspect='auto')

    rect = UpdatingRect.UpdatingRect([0, 0], 0, 0, facecolor='None',
                                     edgecolor='black', linewidth=1.0)
    rect.set_bounds(*ax2.viewLim.bounds)
    ax1.add_patch(rect)

    # Disable zooming into plot 1
    ax1.set_navigate(False)

    ax2.callbacks.connect('xlim_changed', rect)
    ax2.callbacks.connect('ylim_changed', rect)
    ax2.callbacks.connect('xlim_changed', md.ax_update)
    ax2.callbacks.connect('ylim_changed', md.ax_update)
    ax2.set_title("Zoom here")

    # Create canvas and toolbar
    canvas = FigureCanvasTkAgg(fig1, top)
    toolbar = CustomToolbar.CustomToolbar(canvas, top)

    # Book keeping
    canvases.append(canvas)
    toolbars.append(toolbar)

    # Packing the toolbar and plot into the canvas
    toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    return

def nano_analyze(data):
	afmimg, hull_points, wire_with_line, profile = ND.top_level(np.uint8(data[::-1]))
	fig, (ax1,ax2, ax3) = plt.subplots(1, 3)
	ax1.matshow(wire_with_line, cmap=color_code, aspect='auto')
	ax2.matshow(afmimg, cmap=color_code, aspect='auto')
	ax2.scatter(hull_points[:,0],hull_points[:,1], c='white')
	ax3.plot(profile)
	# Create canvas and toolbar
	top = tk.Toplevel()
	top.geometry('{}x{}'.format(800, 500))
	top.title("Nanowire detection results")
	canvas = FigureCanvasTkAgg(fig, top)
	
	# Packing the toolbar and plot into the canvas
	canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	return

def remove_background():
	"""Uses Wes's implementation to remove background from image"""

	backgrounded, background = backgroundremoval.backgroundremoval(np.uint8(md.subset))
	
	top = tk.Toplevel()
	top.title("Backgrounding results")
	top.configure(background='#f7fcb9')
	top.geometry('{}x{}'.format(800, 500))

	button1 = tk.Button(top, text="Dismiss Changes", command=top.destroy)
	button1.pack()
	button2 = tk.Button(top, text="Accept Background and Analyze", command=lambda: nano_analyze(backgrounded))
	button2.pack()
	
	plt.rcParams.update(params)
	fig, (ax1,ax2) = plt.subplots(1, 2)
	ax1.matshow(backgrounded, origin='lower', cmap=color_code, aspect='auto')
	ax1.set_title("Backgrounded image")
	ax2.matshow(background, origin='lower', cmap=color_code, aspect='auto')
	ax2.set_title("Background of image")
	
	# Create canvas and toolbar
	canvas = FigureCanvasTkAgg(fig, top)
	
	# Packing the toolbar and plot into the canvas
	canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	
	return


def recolor(color_selection):
    global color_code
    color_code = color_selection

    global md
    clear_canvas()
    plot_data(md)

    return


def open_webpage(url):
    webbrowser.open_new(url)
    return


def update_status(message):
    """Status updates to the user
    Note: Previous status updates are deleted."""

    # Checking and deleting previous labels
    if len(labels) > 0:
        for label in labels:
            label.destroy()

    # Configuring the new label
    label = tk.Label(top, text=message)
    label.pack()
    labels.append(label)

    return


def process_opencv():

    update_status("Processing image in OpenCV. Please wait ...")

    # ADD PROCESSING CODE HERE

    update_status("OpenCV done")

    return


def process_second():

    update_status("Processing image in OpenCV. Please wait ...")

    update_status("Second algorithm done")

    return


def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, *sys.argv)

params = {
        'axes.labelsize': 12,
        'font.size': 12,
        'legend.fontsize': 12,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'axes.facecolor': 'CCCCCC',
        'figure.facecolor': '#f7fcb9',
        'text.usetex': False,
        'figure.figsize': [5.0, 3.5]}




# FOR BOOK KEEPING
# Maintaining all the labels here
labels = []
# Maintaining all the canvases here
canvases = []
# Maintaining all the toolbars here
toolbars = []
# Input file
md = 0
color_code = 'viridis'
# Ranges
xmin, xmax=0.0,0.0
ymin, ymax=0.0,0.0


# CONFIGURING THE GUI OBJECT
top = tk.Tk()
# Background color
top.configure(background='#f7fcb9')
# Name of program
top.title("NaRWHAL: Nanowire Recognition of Width and Height Analytical Library")
# Size of window
top.geometry('{}x{}'.format(800, 500))
# Exits when you hit Esc
top.bind("<Escape>", lambda e: e.widget.quit())

# Creating a menubar
menubar = tk.Menu(top)

file_menu = tk.Menu(top, tearoff=0)
file_menu.add_command(label="Upload", command=upload_file)
doc_url = "https://github.com/wesleyktatum/Nanowire_Measurements"
file_menu.add_command(
    label="Documentation",
    command=lambda: open_webpage(doc_url))
file_menu.add_command(label="Quit    [Esc]", command=top.quit)
menubar.add_cascade(label="File", menu=file_menu)

# Nanowire Detection menu
process_menu = tk.Menu(top, tearoff=0)
process_menu.add_command(
    label="Process in opencv Algorithm",
    command=process_opencv)
process_menu.add_command(
    label="Process in opencv Algorithm",
    command=process_opencv)
menubar.add_cascade(label="Nanowire Detection", menu=process_menu)

# Color sub-menu
color_menu = tk.Menu(top, tearoff=0)
color_menu.add_command(
    label="Viridis",
    command=lambda: recolor('viridis'))
color_menu.add_command(
    label="Inferno",
    command=lambda: recolor('inferno'))
color_menu.add_command(
    label="Plasma",
    command=lambda: recolor('plasma'))
color_menu.add_command(
    label="Magma",
    command=lambda: recolor('magma'))

# Image Manipulation menu
correct_menu = tk.Menu(top, tearoff=0)
correct_menu.add_command(
    label="Background slope removal",
    command=remove_background)
correct_menu.add_cascade(
    label="Colors",
    menu=color_menu)
menubar.add_cascade(label="Image Manipulation", menu=correct_menu)


# Configuring the window with menubar
top.config(menu=menubar)
top.mainloop()
