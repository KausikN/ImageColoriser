'''
Greyscale to RGB mapping based analysis

(0.3 * R) + (0.59 * G) + (0.11 * B)
'''

# Imports
import cv2
import json
import pickle
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# Util Functions
def ConvertMatchesDict2List(matches, rangeVal=[0, 256, 1]):
    matches_list = []
    for i in range(rangeVal[0], rangeVal[1], rangeVal[2]):
        matches_list.append(matches[str(i)])
    return matches_list

# Main Functions
def GetRGB2GreyscaleCombinationCount(val):
    coeffs = [0.3, 0.59, 0.11]

    combinations = []
    count = 0
    for R in tqdm(range(0,256)):
        for G in range(0,256):
            for B in range(0,256):
                g_val = (coeffs[0]*R) + (coeffs[1]*G) + (coeffs[2]*B)
                if int(round(g_val)) == val:
                    count += 1
                    combinations.append([R, G, B])
    return count, combinations

def GetRGB2GreyscaleCombinationCount_Fast(val):
    coeffs = [0.3, 0.59, 0.11]

    g_combinations = np.arange(0, 256)
    allRGBCombinations = np.array(np.meshgrid(g_combinations, g_combinations, g_combinations)).T.reshape(-1, 3)
    greyScaleVals = (coeffs[0]*allRGBCombinations[:, 0]) + (coeffs[1]*allRGBCombinations[:, 1]) + (coeffs[2]*allRGBCombinations[:, 2])
    gVals_Rounded = np.round(np.array(greyScaleVals, dtype=int))
    matchMask = (gVals_Rounded == val)
    matchedCombinations = allRGBCombinations[matchMask]
    count = int(matchedCombinations.shape[0])

    return count, matchedCombinations

def GetMatchCounts(vals, max_combinations=-1):
    matches = {}
    combinations = {}
    for val in tqdm(vals):
        m, c = GetRGB2GreyscaleCombinationCount_Fast(val)
        matches[str(int(val))] = m
        combinations[str(int(val))] = c
    return matches, combinations

def TruncateCombinations(combinations, max_combinations=-1, method='random'):
    if max_combinations <= -1:
        return combinations

    combinations_t = {}
    matches_t = {}
    for k in tqdm(combinations.keys()):
        l = len(list(combinations[k]))
        c = []
        if max_combinations > l:
            c = combinations[k]
        elif method == 'random':
            ind = np.random.randint(0, l, size=max_combinations)
            c = list(np.array(combinations[k])[ind])
        elif method == 'last':
            c = combinations[k][-max_combinations:]
        elif method == 'mid':
            c = combinations[k][max(0, int(max_combinations/2)):min(l, int(max_combinations/2) + max_combinations)]
        else:
            c = combinations[k][:max_combinations]
        combinations_t[k] = c
        matches_t[k] = len(list(c))
    
    return combinations_t, matches_t

# Driver Code
# Params
# greyScaleValue = 176

# matchesJsonPath = 'ColorisationMethods/Clustering/Data/MatchValues.json'
# combinationsJsonPath = 'ColorisationMethods/Clustering/Data/CombinationValues.p'
# Params

# RunCode
# Get Matches for a value
# Count, Combinations = GetRGB2GreyscaleCombinationCount(greyScaleValue)
# print("GreyScale Value:", greyScaleValue)
# print("Combinations Count:", Count)

# Count, Combinations = GetRGB2GreyscaleCombinationCount_Fast(greyScaleValue)
# print("GreyScale Value:", greyScaleValue)
# print("Combinations Count:", Count)

# Get matches for all values
# allValues = np.arange(0, 256)
# matches, combinations = GetMatchCounts(allValues)
# json.dump(matches, open(matchesJsonPath, 'w'))
# pickle.dump(combinations, open(combinationsJsonPath, 'wb'))

# Load JSON Values
# matches = json.load(open(matchesJsonPath, 'r'))
# combinations = pickle.load(open('ColorisationMethods/Clustering/Data/CombinationValues_Large.p', 'rb'))

# # # Plot Data
# # matches_list = ConvertMatchesDict2List(matches)
# # plt.bar(list(range(0, 256)), matches_list)
# # plt.show()

# # Truncate Combinations
# combinations_t, matches_t = TruncateCombinations(combinations, max_combinations=2500, method='random')

# # Save
# json.dump(matches_t, open('ColorisationMethods/Clustering/Data/MatchValues.json', 'w'))
# pickle.dump(combinations_t, open('ColorisationMethods/Clustering/Data/CombinationValues.p', 'wb'))