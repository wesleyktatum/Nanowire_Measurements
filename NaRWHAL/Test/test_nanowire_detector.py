import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
%matplotlib inline
import skimage.measure
import nanowire_detector

def test_top_level():
    '''this is the function through which all other functions
    are called'''
    afmimg = np.loadtxt('afmimg_test.txt')
    assert afmimg.all() != 0
    assert afmimg
    afmimg,hull_points,wire_with_line,profile = nanowire_detector.top_level(afmimg)
    assert hull_points
    assert wire_with_line
    assert profile

def test_afm_copier():
    '''this makes a copy of the snipped and backgrounded afm image'''
    afmimg = np.loadtxt('afmimg_test.txt')
    assert afmimg.all() != 0
    assert afmimg
    image_copy = nanowire_detector.afm_copier(afmimg)
    assert image_copy.all() != 0

def test_contour_finder():
    '''Here we use a threshold to find the contours
    of the selected image.'''
    # now determine the threshold - we choose half the max intensity
    afmimg = np.loadtxt('afmimg_test.txt')
    copied_image = np.copy(afmimg)
    assert afmimg.all() != 0
    contours = nanowire_detector.contour_finder(coped_image)
    assert contours

def test_convex_hull_determiner():
    '''This uses the calculated contours to determine
    the existence of a convex hull (i.e. a nanowire)'''
    # This turns the contours into an array of points
    afmimg = np.loadtxt('afmimg_test.txt')
    copied_image = np.copy(afmimg)
    assert afmimg.all() != 0
    contours = nanowire_detector.contour_finder(coped_image)
    cnts, hull = nanowire_detector.convex_hull_determiner(afmimg,contours)
    assert cnts
    assert hull

def test_draw_line():
    '''Here we use the convex hull to fit a line along
    the nanowire, and then switch the indeces so that
    the line lies along the short axis of the wire'''
    

def test_wire_profile():
    '''Now we compute the profile and adjust to real units'''
    righty = [0,0]
    lefty = [0,0]
    if (righty==lefty).all():
        assert "no line drawn"
    profile = skimage.measure.profile_line(afmimg,(righty,0),(lefty,cols-1))
    return profile
