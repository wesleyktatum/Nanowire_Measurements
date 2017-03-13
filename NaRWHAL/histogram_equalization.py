import cv2
import numpy as np

def histogram_equalization(source):
    """
    Takes in a uint8 image and equalizes the histogram
    """
    img = source
    equ = cv2.equalizeHist(img)
    
    return equ
