#Creates two identical panels.  Zooming in on the right panel will show
# a rectangle in the first panel, denoting the zoomed region.
import numpy as np, sys
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import filedialog
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


# We just subclass Rectangle so that it can be called with an Axes
# instance, causing the rectangle to update its shape to match the
# bounds of the Axes
class UpdatingRect(Rectangle):
    def __call__(self, ax):
        self.set_bounds(*ax.viewLim.bounds)
        ax.figure.canvas.draw_idle()


# A class that will regenerate a fractal set as we zoom in, so that you
# can actually see the increasing detail.  A box in the left panel will show
# the area to which we are zoomed.
class MandelbrotDisplay(object):
    def __init__(self, h=500, w=500, d='part1.txt'):
        self.height = h
        self.width = w
        #self.data=np.genfromtxt(sys.argv[1])
        self.data=np.genfromtxt(d)
        
    def __call__(self, xstart, xend, ystart, yend):
        threshold_time=self.data[int(ystart):int(yend), int(xstart):int(xend)]
        return threshold_time

    def ax_update(self, ax):
        ax.set_autoscale_on(False)  # Otherwise, infinite loop

        # Get the number of points from the number of pixels in the window
        dims = ax.axesPatch.get_window_extent().bounds
        self.width = int(dims[2] + 0.5)
        self.height = int(dims[2] + 0.5)

        # Get the range for the new area
        xstart, ystart, xdelta, ydelta = ax.viewLim.bounds
        xend = xstart + xdelta
        yend = ystart + ydelta

        # Update the image object with our new data and extent
        im = ax.images[-1]
        im.set_data(self.__call__(xstart, xend, ystart, yend))
        im.set_extent((xstart, xend, ystart, yend))
        ax.figure.canvas.draw_idle()

def upload_file():
    """ Upload the chosen file and plot the nanowire image onto the canvas"""

    filename = filedialog.askopenfilename() #upload file
    #afmdata=np.genfromtxt(filename)
    md = MandelbrotDisplay(d=filename)
    xmax, ymax = np.shape(md.data)
    Z = md(0,xmax,0,ymax)
    fig1, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(Z, origin='lower', extent=(0,xmax,0,ymax))
    ax2.imshow(Z, origin='lower', extent=(0,xmax,0,ymax))
    
    rect = UpdatingRect([0, 0], 0, 0, facecolor='None', edgecolor='black', linewidth=1.0)
    rect.set_bounds(*ax2.viewLim.bounds)
    ax1.add_patch(rect)
    ax2.callbacks.connect('xlim_changed', rect)
    ax2.callbacks.connect('ylim_changed', rect)
    ax2.callbacks.connect('xlim_changed', md.ax_update)
    ax2.callbacks.connect('ylim_changed', md.ax_update)
    ax2.set_title("Zoom here")
    #plt.show()
    
    
    canvas = FigureCanvasTkAgg(fig1, top) #create canvas
    canvas.show()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2TkAgg(canvas, top) #create navigation tool bar that contains the zoom-in/crop option
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.TOP)
    
    return

def process_opencv():
    var = tk.StringVar()
    label = tk.Label(top, textvariable=var)
    var.set("In the process of opencv algorithm")
    label.pack()
    return

def process_second():
    var = tk.StringVar()
    label = tk.Label(top, textvariable=var)
    var.set("In the process of second algorithm")
    label.pack()
    return

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

top = tk.Tk()
B = tk.Button(top, text="Upload", command = upload_file)
A = tk.Button(top, text="Process in opencv Algorithm", command = process_opencv)
C = tk.Button(top, text="Process in second Algorithm", command = process_second)
D = tk.Button(top, text="Restart", command = restart_program)
#create the buttons

B.pack()
C.pack(side="bottom")
A.pack(side="bottom") #set the position of process button to always at the bottom
D.pack()
top.mainloop() 



