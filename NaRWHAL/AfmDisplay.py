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


class AfmDisplay(object):

    def __init__(self, h=500, w=500, d=''):
        """Initialize variables"""

        self.height = h
        self.width = w
        self.data = np.uint8(np.copy(d))
        self.subset = np.uint8(np.copy(d))

    def __call__(self, xstart, xend, ystart, yend):
        """Crops user-image according to zoomed data"""

        self.subset = self.data[
            int(ystart):int(yend),
            int(xstart):int(xend)]
        return self.subset

    def ax_update(self, ax):
        """Updates the figure axes to zoom in"""

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
