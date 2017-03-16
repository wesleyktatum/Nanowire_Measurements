# Creates two identical panels.  Zooming in on the right panel will show
# a rectangle in the first panel, denoting the zoomed region.
import numpy as np
import sys
import os
import webbrowser
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog, Scrollbar, Text
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import AfmDisplay
import CustomToolbar
import UpdatingRect
import backgrounding as BR
import nanowire_detector as ND


def clear_canvas():
    """Deletes previous canvases"""

    if len(toolbars) > 0:
        toolbars[-1].destroy()

    if len(canvases) > 0:
        canvases[-1].get_tk_widget().delete("all")
        canvases[-1].get_tk_widget().destroy()

    if len(msgs) > 0:
        msgs[-1].destroy()
        msgs[-2].destroy()
    return


def normalize_data(file_data):
    """Converting range of data from 0-255."""

    # Changing the range of data to 0 ...
    min_d = np.min(file_data)
    file_data = file_data - min_d
    file_data = file_data * (255.0) / np.max(file_data)

    return file_data


def upload_file():
    """ Upload the chosen file and plot the nanowire image onto the canvas"""

    global filename
    filename = filedialog.askopenfilename()
    file_data = np.genfromtxt(filename)
    file_data = normalize_data(file_data)

    global md
    md = AfmDisplay.AfmDisplay(d=file_data)
    plot_data(md)

    global correct_menu
    # Enable menus now that there's an image to work on
    correct_menu.entryconfig(0, state=tk.NORMAL)
    correct_menu.entryconfig(1, state=tk.NORMAL)

    return


def plot_data(md):
    """Plotting the 2-piece plot to show original image"""

    xmax, ymax = np.shape(md.data)

    clear_canvas()

    plt.rcParams.update(params)

    fig1, (ax1, ax2) = plt.subplots(1, 2)

    ax1.matshow(
        md.data,
        origin='lower',
        extent=(
            0,
            xmax,
            0,
            ymax),
        cmap=color_code,
        aspect='auto')
    ax2.matshow(
        md.data,
        origin='lower',
        extent=(
            0,
            xmax,
            0,
            ymax),
        cmap=color_code,
        aspect='auto')

    rect = UpdatingRect.UpdatingRect([0, 0], 0, 0, facecolor='None',
                                     edgecolor='black', linewidth=1.0)
    rect.set_bounds(*ax2.viewLim.bounds)
    ax1.add_patch(rect)

    # Disable zooming into plot 1
    ax1.set_navigate(False)
    ax1.set_title("Reference AFM Image")
    ax1.xaxis.set_tick_params(labeltop='off', labelbottom='on')

    ax2.callbacks.connect('xlim_changed', rect)
    ax2.callbacks.connect('ylim_changed', rect)
    ax2.callbacks.connect('xlim_changed', md.ax_update)
    ax2.callbacks.connect('ylim_changed', md.ax_update)
    ax2.xaxis.set_tick_params(labeltop='off', labelbottom='on')
    ax2.set_title("Zoom into a single nanowire here")

    # Create canvas and toolbar
    canvas = FigureCanvasTkAgg(fig1, top)
    toolbar = CustomToolbar.CustomToolbar(canvas, top)
    msg1 = tk.Message(
        top,
        justify=tk.CENTER,
        text="Showing file:\n" +
        filename,
        width=800,
        aspect=1000,
        background='#f7fcb9')

    # Book keeping
    canvases.append(canvas)
    toolbars.append(toolbar)

    # Packing the toolbar and plot into the canvas
    msg1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar.pack(side=tk.TOP, fill=tk.X, anchor=tk.CENTER)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    msg2 = tk.Message(
        top,
        width=700,
        aspect=1000,
        justify=tk.CENTER,
        background='#f7fcb9',
        text="Zoom into your preferred nanowire on the right image or reset (Home symbol).\n When you've selected a region with a single nanowire, initialize analysis by Image Processing->Background slope removal.\n You can also choose your favorite color scheme from above (Image Processing->Color).")
    msg2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    msgs.append(msg1)
    msgs.append(msg2)

    return


def nano_analyze(data):
    """Calculating height profile of nanowire and detecting outline"""

    data = normalize_data(data)

    afmimg, hull_points, wire_with_line, profile = ND.top_level(
        np.uint8(data[::-1]))

    # afmimg, hull_points, wire_with_line, profile = ND.top_level(
    #    np.uint8(255-data[::-1]))
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ax1.matshow(wire_with_line, cmap=color_code, aspect='auto')
    ax1.set_title("Line along cross-section of wire")
    ax1.xaxis.set_tick_params(labeltop='off', labelbottom='on')

    ax3.matshow(afmimg, cmap=color_code, aspect='auto')
    ax3.set_title("Outline of nanowire")
    ax3.xaxis.set_tick_params(labeltop='off', labelbottom='on')
    ax3.scatter(hull_points[:, 0], hull_points[:, 1], c='white')

    ax2.plot(profile)
    ax2.set_title("Height profile along the line")
    ax2.xaxis.set_tick_params(labeltop='off', labelbottom='on')

    # Create canvas and toolbar
    top = tk.Toplevel()
    top.geometry('{}x{}'.format(1000, 500))
    top.title("Nanowire detection results")
    canvas = FigureCanvasTkAgg(fig, top)
    msg = tk.Message(
        top,
        text="The algorithm detects single nanowires in the given snippet. It makes a line perpendicular to the wire and calculates the height of points along the line. The algorithm also detects and outline of the nanowire",
        width=800,
        aspect=1000,
        justify=tk.CENTER,
        background='#f7fcb9')

    # Packing the toolbar and plot into the canvas
    msg.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    return


def remove_background():
    """Detecting and removing gradient background (only) from image"""

    backgrounded, background = BR.backgroundremoval(
        np.uint8(md.subset))

    top = tk.Toplevel()
    top.title("Backgrounding results")
    top.configure(background='#f7fcb9')
    top.geometry('{}x{}'.format(800, 500))

    msg = tk.Message(
        top,
        width=800,
        aspect=1000,
        background='#f7fcb9',
        justify=tk.CENTER,
        text="The algorithm removes perceptible slopes from the background of the image")
    msg.pack(side=tk.TOP, fill=tk.X, expand=1)

    button1 = tk.Button(top, text="Dismiss Changes", command=top.destroy)
    button1.pack()
    button2 = tk.Button(
        top,
        text="Accept Background and Analyze",
        command=lambda: nano_analyze(backgrounded))
    button2.pack()

    plt.rcParams.update(params)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.matshow(backgrounded, origin='lower', cmap=color_code, aspect='auto')
    ax1.set_title("Image after processing")
    ax1.xaxis.set_tick_params(labeltop='off', labelbottom='on')
    ax2.matshow(background, origin='lower', cmap=color_code, aspect='auto')
    ax2.xaxis.set_tick_params(labeltop='off', labelbottom='on')
    ax2.set_title("Background noise removed from image")

    # Create canvas and toolbar
    canvas = FigureCanvasTkAgg(fig, top)

    # Packing the toolbar and plot into the canvas
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    return


def hist_equalizer():
    """Equalizing the colors in the image"""
    return


def recolor(color_selection):
    """Recolor the plots according to user selection"""

    global color_code
    color_code = color_selection

    global md
    plot_data(md)

    return


def open_readme():
    """Open user documentation"""

    window = tk.Toplevel()
    window.title('Documentation')
    scrollbar = Scrollbar(window)
    scrollbar.pack(side="right", fill="y")
    text = Text(window, wrap="word", yscrollcommand=scrollbar.set)
    readme = open('../README.md', 'r')
    text.insert("end", readme.read())
    text.config(font="Times", background="lightblue")
    text.pack()
    scrollbar.config(command=text.yview)

    return


params = {
    'axes.labelsize': 12,
    'font.size': 10,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'axes.facecolor': 'CCCCCC',
    'figure.facecolor': '#f7fcb9',
    'text.usetex': False,
    'figure.figsize': [5.0, 3.5]}


# FOR BOOK KEEPING
# Maintaining all the labels here
msgs = []
# Maintaining all the canvases here
canvases = []
# Maintaining all the toolbars here
toolbars = []
# Input file
md = 0
color_code = 'viridis'
filename = ''


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
file_menu.add_command(label="Documentation", command=open_readme)
file_menu.add_command(label="Quit    [Esc]", command=top.quit)
menubar.add_cascade(label="File", menu=file_menu)

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

bkg_menu = tk.Menu(top, tearoff=0)
bkg_menu.add_command(
    label="Correct Contrast",
    command=hist_equalizer)
bkg_menu.add_command(
    label="Remove Background Slope",
    command=remove_background)


# Image Manipulation menu
correct_menu = tk.Menu(top, tearoff=0)
correct_menu.add_cascade(
    label="Background Correction",
    menu=bkg_menu)
correct_menu.add_cascade(
    label="Colors",
    menu=color_menu)
menubar.add_cascade(label="Image Processing", menu=correct_menu)

# Disabling menus since image hasn't been uploaded yet
correct_menu.entryconfig(0, state=tk.DISABLED)
correct_menu.entryconfig(1, state=tk.DISABLED)


# Configuring the window with menubar
top.config(menu=menubar)
top.mainloop()
