'''
Thresholding based Image Coloriser
'''

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt

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

# Main Vars


# Main Functions
##### Simple Thresholding Colorisation ################################################################
def ColoriseImage_ThresholdingSimple(I=None, imgPath=None, thresholds=[], thresholdColors=[], defaultColor=[0, 0, 0]):
    if I is None:
        I = ReadImage(imgPath, greyScale=True)

    I_c = np.ones((I.shape[0], I.shape[1], 3), dtype=int) * defaultColor
    for i in range(len(thresholds)):
        I_c[I >= thresholds[i]] = thresholdColors[i]

    return I_c
    
##### Simple Thresholding Colorisation ################################################################

# Driver Code
# # Params
# imgPath = 'Examples/AndhaNaal.PNG'

# imgSize = (100, 100)
# # Params

# # # RunCode
# # Load Inputs
# print("Loading Image Inputs...")
# I_grey = ReadImage(imgPath, greyScale=True, size=imgSize)

# # Colorise input image
# print("Colorising Image...")
# I_color = ColoriseImage_ClusteringRandom(I=I_grey)

# # Plot Results
# plt.subplot(1, 2, 1)
# plt.imshow(I_grey, 'gray')
# plt.subplot(1, 2, 2)
# plt.imshow(I_color)
# plt.show()