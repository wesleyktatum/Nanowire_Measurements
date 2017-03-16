import cv2
from skimage import color
from skimage import exposure
from photutils import Background2D, SigmaClip, MedianBackground
import numpy as np

def background_removal(afmdata):
    """
    A function to remove gradients in the background of AFM micrographs. Takes in a .txt source file and returns the
    image as a numpy array with the background gradient removed.
    """
    # Generate a numpy array from the .txt file and convert values from m to nm

    height, width = afmdata.shape

    # Remove any background that is greater than 3 stddevs from the mean.
    # Removes gradients in the image.
    sigma_clip = SigmaClip(sigma=3., iters=10)
    bkg_estimator = MedianBackground()
    bkg = Background2D(afmdata, (50, 50), filter_size=(
        3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
    backgrounded = afmdata - bkg.background

    return [backgrounded, bkg.background]


def histogram_equalization(source):
    """
    Takes in a uint8 image and equalizes the histogram
    """
    img = source
    equ = cv2.equalizeHist(img)

    return equ
