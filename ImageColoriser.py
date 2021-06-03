'''
Image Coloriser for converting greyscale and black and white images and video to color
'''

# Imports
import cv2

from ColorisationMethods.Clustering import ImageColoriser_Clustering
from ColorisationMethods.Thresholding import ImageColoriser_Thresholding

# Main Vars

# Util Functions
def ReadImage(imgPath, greyScale=False, size=None):
    I = None
    if greyScale:
        I = cv2.imread(imgPath, 0)
    else:
        I = cv2.imread(imgPath)
    if size is not None:
        I = cv2.resize(I, size)
    return I

# Main Functions


# Driver Code