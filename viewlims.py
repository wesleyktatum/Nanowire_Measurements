#Creates two identical panels.  Zooming in on the right panel will show
# a rectangle in the first panel, denoting the zoomed region.
import numpy as np, sys, os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import filedialog
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class CustomToolbar(NavigationToolbar2TkAgg):
    """Creates custom toolbar"""
    def __init__(self,canvas_,parent_):
        self.toolitems = (
            ('Zoom', 'Manually zoom into image', 'zoom_to_rect', 'zoom'),
            ('Home', 'Revert to original image', 'home', 'home'),
            )
        NavigationToolbar2TkAgg.__init__(self,canvas_,parent_)

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

def clear_canvas():
    """Deletes previous canvases"""
    if len(canvases) > 0 : 
        for canvas in canvases: 
            canvas.get_tk_widget().delete("all")
            canvas.get_tk_widget().destroy()
    if len(toolbars) > 0 : 
        for toolbar in toolbars: 
            toolbar.destroy()
    return

def upload_file():
    """ Upload the chosen file and plot the nanowire image onto the canvas"""

    filename = filedialog.askopenfilename() #upload file
    
    md = MandelbrotDisplay(d=filename)
    xmax, ymax = np.shape(md.data)
    
    clear_canvas()
    
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
    
    
    canvas = FigureCanvasTkAgg(fig1, top) #create canvas
    canvases.append(canvas)
    canvas.show()
    canvas.get_tk_widget().pack()
    
    # Create navigation tool bar that contains the zoom-in/crop option
    toolbar = CustomToolbar(canvas, top) 
    toolbar.update()
    toolbars.append(toolbar)
    canvas._tkcanvas.pack(side=tk.TOP)

    
    return

def update_status(message):
    """Status updates to the user
    Note: Previous status updates are deleted."""
    
    # Checking and deleting previous labels
    if len(labels) > 0:
        for label in labels: label.destroy()
            
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
labels=[]
# Maintaining all the canvases here
canvases=[]
# Maintaining all the toolbars here
toolbars=[]
    
# CONFIGURING THE GUI OBJECT
top = tk.Tk()
# Background color
top.configure(background='#f7fcb9')
# Name of program
top.title("NaRWHAL: Nanowire Recognition of Width and Height Analytical Library")
# Size of window
top.geometry('{}x{}'.format(1000, 800))
# Exits when you hit Esc
top.bind("<Escape>", lambda e: e.widget.quit())




#create the buttons
B = tk.Button(top, text="Upload", command = upload_file)
A = tk.Button(top, text="Process in opencv Algorithm", command = process_opencv)
C = tk.Button(top, text="Process in second Algorithm", command = process_second)
D = tk.Button(top, text="Restart", command = clear_canvas)



B.pack()
C.pack(side="bottom")
A.pack(side="bottom") #set the position of process button to always at the bottom
D.pack()
top.mainloop() 



