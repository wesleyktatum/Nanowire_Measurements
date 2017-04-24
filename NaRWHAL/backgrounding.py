import cv2
from skimage import color
from skimage import exposure
from photutils import Background2D, SigmaClip, MedianBackground
import numpy as np

def background_removal(afmdata, n = 3):
    """
    This function takes in a raw spectra as a .txt file and a user desired degree, n, of polynomial
    fitting. The default value for n is 3. It returns the background data and the backgrounded data as np arrays
    """
    import warnings
    import numpy as np
    import matplotlib.pyplot as plt
    from astropy.modeling import models, fitting
    
    p_init = models.Polynomial2D(degree = n)
    fit_p = fitting.LevMarLSQFitter()
    
    x, y = afmdata.shape
    
    yy, xx = np.mgrid[0:x, 0:y]

    with warnings.catch_warnings():
        # Ignore model linearity warning from the fitter
        warnings.simplefilter('ignore')
        p = fit_p(p_init, xx, yy, afmdata)
    
    bkg = p(xx, yy)
    final = afmdata - bkg
    
    return [final, bkg]


def histogram_equalization(source):
    """
    Takes in a uint8 image and equalizes the histogram
    """
    img = source
    equ = cv2.equalizeHist(img)

    return equ

 #   """
  #  A function to remove gradients in the background of AFM micrographs. Takes in a .txt source file and returns the
   # image as a numpy array with the background gradient removed.
#    """
    # Generate a numpy array from the .txt file and convert values from m to nm
#
#    height, width = afmdata.shape

    # Remove any background that is greater than 3 stddevs from the mean.
    # Removes gradients in the image.
 #   sigma_clip = SigmaClip(sigma=3., iters=10)
  #  bkg_estimator = MedianBackground()
   # bkg = Background2D(afmdata, (50, 50), filter_size=(
    #    3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
#    backgrounded = afmdata - bkg.background
#
 #   return [backgrounded, bkg.background]
#
#def polynm_background(raw, n):
