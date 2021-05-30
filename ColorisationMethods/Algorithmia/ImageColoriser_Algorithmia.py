'''
Algorithmia API Coloriser
'''

# Imports
import Algorithmia
import json
import cv2

# Main Vars
config = json.load(open('ColorisationMethods/Algorithmia/Data/config.json', 'r'))
ALGO_INPUT_IMGPATH = 'ColorisationMethods/Algorithmia/Inputs/GreyImage.png'

CLIENT = None
ALGO_COLORISER = None

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

def LoadImageInput(I):
    cv2.imwrite(ALGO_INPUT_IMGPATH, I)

# Main Functions
##### Algorithmia Colorisation ################################################################
def InitColoriserClient():
    global CLIENT
    global ALGO_COLORISER

    CLIENT = Algorithmia.client(config['API_KEY'])
    ALGO_COLORISER = CLIENT.algo(config['ALGO_COLORISER_KEY'])
    ALGO_COLORISER.set_options(timeout=100)

def ColoriseImage_Algorithmia(imgPath):
    # Prepare Input
    inputData = {
    "image": imgPath#"data://deeplearning/example_data/lincoln.jpg"
    }
    return ALGO_COLORISER.pipe(inputData)
##### Algorithmia Colorisation ################################################################

# Driver Code
# # Params
# imgPath = 'Examples/AndhaNaal.PNG'

# imgSize = (100, 100)
# # Params

# # RunCode
# # Init Coloriser
# print("Initialising Algorithmia client and algorithm...")
# InitColoriserClient()

# # Load Inputs
# print("Loading Image Inputs...")
# I_grey = ReadImage(imgPath, greyScale=True, size=imgSize)
# LoadImageInput(I_grey)

# # Colorise input image
# print("Colorising Image...")
# outputData = ColoriseImage_Algorithmia(ALGO_INPUT_IMGPATH)
# print(outputData)
# print(outputData.result)