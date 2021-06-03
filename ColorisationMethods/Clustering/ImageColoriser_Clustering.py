'''
Clustering based Image Coloriser
'''

# Imports
import pickle
import json
import cv2
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# Util Functions
def ReadJSON(path):
    return json.load(open(path, 'r'))

def ReadPickle(path):
    return pickle.load(open(path, 'rb'))

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
PATH_MATCHES = 'ColorisationMethods/Clustering/Data/MatchValues.json'
PATH_COMBINATIONS = 'ColorisationMethods/Clustering/Data/CombinationValues.p'

print("Loading Matches and Combinations...")
MATCHES = ReadJSON(PATH_MATCHES)
COMBINATIONS = ReadPickle(PATH_COMBINATIONS)

MAPPING_METHODS = ['Random', 'First', 'Middle', 'Last']

# Main Functions
##### Clustering Simple Colorisation ################################################################
def ColoriseImage_ClusteringSimple(I=None, imgPath=None, COMBINATIONS=COMBINATIONS, method='random'):
    if I is None:
        I = ReadImage(imgPath, greyScale=True)
    
    I_c = np.zeros((I.shape[0], I.shape[1], 3), dtype=np.uint8)

    uniqueValues = np.unique(np.reshape(I, (-1)))
    for uV in tqdm(uniqueValues):
        mask = (I == uV)
        # Get Random Matching Combination
        matchComb = [0, 0, 0]
        if str(uV) in MATCHES.keys():
            if method == 'random':
                matchComb = COMBINATIONS[str(uV)][np.random.randint(0, MATCHES[str(uV)])]
            elif method == 'last':
                matchComb = COMBINATIONS[str(uV)][-1]
            elif method == 'middle':
                l = len(list(COMBINATIONS[str(uV)]))
                matchComb = COMBINATIONS[str(uV)][int(l/2)]
            else:
                matchComb = COMBINATIONS[str(uV)][0]
        # Set Value
        I_c[mask] = matchComb

    return I_c
##### Clustering Simple Colorisation ################################################################

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