import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import skimage.measure


def top_level(afmimg):
    '''this is the function through which all other functions
    are called'''
    copy = afm_copier(afmimg)
    contours = contour_finder(copy)
    contour_points, hull_points = convex_hull_determiner(afmimg, contours)
    wire_with_line, right_point, left_point, num_cols = draw_line(
        contour_points, afmimg, copy)
    profile = wire_profile(afmimg, right_point, left_point, num_cols)
    return afmimg, hull_points, wire_with_line, profile


def afm_copier(afmimg):
    '''this makes a copy of the snipped and backgrounded afm image'''
    image_copy = np.copy(afmimg)
    return image_copy


def contour_finder(copied_image):
    '''Here we use a threshold to find the contours
    of the selected image.'''
    # now determine the threshold - we choose half the max intensity
    ret, thresh = cv2.threshold(copied_image, 145, 255, cv2.THRESH_TOZERO)
    # this determines the contours
    dummy, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def convex_hull_determiner(afmimg, contours):
    '''This uses the calculated contours to determine
    the existence of a convex hull (i.e. a nanowire)'''
    # This turns the contours into an array of points
    cnts = max(contours, key=cv2.contourArea)
    # now we determine whether or not there is a hull
    hull = cv2.convexHull(cnts)
    hull = np.reshape(hull, (len(hull), 2))
    return cnts, hull


def draw_line(cnts, afmimg, copied_image):
    '''Here we use the convex hull to fit a line along
    the nanowire, and then switch the indeces so that
    the line lies along the short axis of the wire'''
    rows, cols = afmimg.shape[:2]
    # Here we fit a line along the nanowire
    [line_x, line_y, int_x, int_y] = cv2.fitLine(
        cnts, distType=2, param=0, reps=0.01, aeps=0.01)
    # this determines the left and right side endpoints of the line...
    lefty = int((-int_x * line_y / line_x) + int_y)
    righty = int(((cols - int_x) * line_y / line_x) + int_y)
    # ...but we inverse the indices, thus generating a perpendular line
    wire_with_line = cv2.line(
        copied_image, (righty, 0), (lefty, cols - 1), (0, 255, 0), 2)
    return wire_with_line, righty, lefty, cols


def wire_profile(afmimg, righty, lefty, cols):
    '''Now we compute the profile and adjust to real units'''
    profile = skimage.measure.profile_line(
        afmimg, (righty, 0), (lefty, cols - 1))
    return profile
