'''
Thresholding based Image Coloriser
'''

# Imports
import numpy as np
from tqdm import tqdm

# Main Functions
def ColoriseImage_Thresholding_RangedGradients(I, intervals=[], **params):
    '''
    Colorise Image based on Ranged Interval Gradients
    '''
    # Init color image
    I_c = np.zeros((I.shape[0], I.shape[1], 3), dtype=float)
    # For each interval
    for intData in intervals:
        # Get interval data
        interval = intData["interval"]
        colorGrad_start, colorGrad_end = np.array(intData["gradient"]["start"]), np.array(intData["gradient"]["end"])
        # Mask and colorize
        mask = (I >= interval[0]) & (I < interval[1])
        maskedVals = np.dstack((I[mask], I[mask], I[mask]))
        I_c[mask] = colorGrad_start + (colorGrad_end - colorGrad_start) * maskedVals

    return I_c

# Main Vars
COLORISERS_THRESHOLDING = {
    "Ranged Gradients": ColoriseImage_Thresholding_RangedGradients
}