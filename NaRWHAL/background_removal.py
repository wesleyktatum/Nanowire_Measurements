from photutils import Background2D, SigmaClip, MedianBackground

from skimage import color
from skimage import exposure

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

def background_removal(source):
    """
    A function to remove gradients in the background of AFM micrographs. Takes in a .txt source file and returns the
    image as a numpy array with the background gradient removed.
    """
    #Generate a numpy array from the .txt file and convert values from m to nm
    afmdata = np.genfromtxt(source)
    afmdata= afmdata*(10**9)
    height, width = afmdata.shape

    #Remove any background that is greater than 3 stddevs from the mean. Removes gradients in the image.
    sigma_clip = SigmaClip(sigma=3., iters=10)
    bkg_estimator = MedianBackground()
    bkg = Background2D(afmdata, (50, 50), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
    backgrounded = afmdata - bkg.background

    return backgrounded
