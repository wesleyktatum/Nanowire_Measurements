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
import AfmDisplay, CustomToolbar, UpdatingRect


def clear_canvas():
    """Deletes previous canvases"""
    if len(canvases) > 0:
        for canvas in canvases:
            canvas.get_tk_widget().delete("all")
            canvas.get_tk_widget().destroy()
    if len(toolbars) > 0:
        for toolbar in toolbars:
            toolbar.destroy()
    return


def upload_file():
    """ Upload the chosen file and plot the nanowire image onto the canvas"""

    filename = filedialog.askopenfilename()  # upload file

    md = AfmDisplay.AfmDisplay(d=filename)
    xmax, ymax = np.shape(md.data)

    clear_canvas()

    Z = md(0, xmax, 0, ymax)

    params = {
        'axes.labelsize': 15,
        'font.size': 15,
        'legend.fontsize': 15,
        'xtick.labelsize': 15,
        'ytick.labelsize': 15,
        'axes.facecolor': 'CCCCCC',
        'figure.facecolor': '#f7fcb9',
        'text.usetex': False,
        'figure.figsize': [5.0, 3.5]}

    plt.rcParams.update(params)

    fig1, (ax1, ax2) = plt.subplots(1, 2)

    ax1.imshow(Z, origin='lower', extent=(0, xmax, 0, ymax))
    ax2.imshow(Z, origin='lower', extent=(0, xmax, 0, ymax))

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
    os.execl(python, python, * sys.argv)

# FOR BOOK KEEPING
# Maintaining all the labels here
labels = []
# Maintaining all the canvases here
canvases = []
# Maintaining all the toolbars here
toolbars = []

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
file_menu.add_command(label="Documentation", command=open_webpage(doc_url))
file_menu.add_command(label="Quit    [Esc]", command=top.quit)
menubar.add_cascade(label="File", menu=file_menu)

process_menu = tk.Menu(top, tearoff=0)
process_menu.add_command(
    label="Process in opencv Algorithm",
    command=process_opencv)
process_menu.add_command(
    label="Process in opencv Algorithm",
    command=process_opencv)
menubar.add_cascade(label="Data Processing", menu=process_menu)

# Configuring the window with menubar
top.config(menu=menubar)
top.mainloop()
