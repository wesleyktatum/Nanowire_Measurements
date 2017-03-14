import backgrounding

import numpy as np

def test_background_removal():
    """
    This function tests the background removal function
    """
    testdata = np.genfromtxt('../Data/UnbackgroundedTXT/5umUniformNetwork')
    bkgd = backgrounding.background_removal(testdata)

    assert bkgd != None, 'Backgrounding has deleted datafile'
    return


def test_histogram_equalization():
    """
    This function tests the histogram equalization function
    """
    
    testdata = np.genfromtxt('../Data/UnbackgroundedTXT/5umUniformNetwork')
    
    equ = backgrounding.histogram_equalization(testdata)
    
    assert equ != None, 'Equalization has deleted datafile'
    return
