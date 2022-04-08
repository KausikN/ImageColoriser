"""
Stream lit GUI for hosting ImageColoriser
"""

# Imports
import cv2
import numpy as np
import streamlit as st
import json

from ImageColoriser import *

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
DEFAULT_PATH_EXAMPLEIMAGE = "TestData/TestImgs/Staircase.png"

COLORISERINDICATORIMAGE_SIZE = [128, 128]
DEFAULT_COLORISER_BASEGRADIENT = {
    "start": [0.0, 0.0, 0.0],
    "end": [0.25, 0.41, 0.88]
}
DEFAULT_COLORISER_THRESHOLDS = [0.25, 0.6, 0.85, 0.95]
DEFAULT_COLORISER_COLORS = [
    [0.93, 0.84, 0.69],
    [0.13, 0.55, 0.13],
    [0.55, 0.54, 0.54],
    [1.0, 0.98, 0.98]
]

# Util Vars
RADIALINDICATORIMAGE = None

# Util Functions
def Hex_to_RGB(val):
    val = val.lstrip('#')
    lv = len(val)
    rgb = tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    rgb = np.array(rgb) / 255.0
    return rgb

def RGB_to_Hex(rgb):
    rgb = np.array(np.array(rgb) * 255, dtype=np.uint8)
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

@st.cache
def GenerateRadialIndicatorImage():
    global RADIALINDICATORIMAGE
    if RADIALINDICATORIMAGE is None:
        # Generate Radial vals
        x_vals = np.linspace(-1.0, 1.0, COLORISERINDICATORIMAGE_SIZE[0])[:, None]
        y_vals = np.linspace(-1.0, 1.0, COLORISERINDICATORIMAGE_SIZE[1])[None, :]
        RADIALINDICATORIMAGE = np.sqrt(x_vals ** 2 + y_vals ** 2)
        RADIALINDICATORIMAGE = 1 - ((RADIALINDICATORIMAGE - np.min(RADIALINDICATORIMAGE)) / (np.max(RADIALINDICATORIMAGE) - np.min(RADIALINDICATORIMAGE)))
    return RADIALINDICATORIMAGE

@st.cache
def GenerateColoriserIndicatorImage_Thresholding(USERINPUT_BaseGradient, USERINPUT_Thresholds, USERINPUT_ThresholdColors):
    RADIALINDICATORIMAGE = GenerateRadialIndicatorImage()
    # Get Intervals
    Intervals = []
    prevVal, prevColor = 0.0, USERINPUT_BaseGradient["start"]
    for i in range(len(USERINPUT_Thresholds)):
        Intervals.append({
            "interval": [prevVal, USERINPUT_Thresholds[i]],
            "gradient": {
                "start": prevColor,
                "end": USERINPUT_ThresholdColors[i]
            }
        })
        prevVal = USERINPUT_Thresholds[i]
        prevColor = USERINPUT_ThresholdColors[i]
    Intervals.append({
        "interval": [prevVal, 1.0],
        "gradient": {
            "start": prevColor,
            "end": USERINPUT_BaseGradient["end"]
        }
    })
    # Get colorised indicator image
    I_ic = ColoriseImage_Thresholding_RangedGradients(RADIALINDICATORIMAGE, intervals=Intervals)

    return I_ic

# Main Functions
# @st.cache
def GenerateColorisedImage_Thresholding(I, USERINPUT_BaseGradient, USERINPUT_Thresholds, USERINPUT_ThresholdColors):
    # Get Intervals
    Intervals = []
    prevVal, prevColor = 0.0, USERINPUT_BaseGradient["start"]
    for i in range(len(USERINPUT_Thresholds)):
        Intervals.append({
            "interval": [prevVal, USERINPUT_Thresholds[i]],
            "gradient": {
                "start": prevColor,
                "end": USERINPUT_ThresholdColors[i]
            }
        })
        prevVal = USERINPUT_Thresholds[i]
        prevColor = USERINPUT_ThresholdColors[i]
    Intervals.append({
        "interval": [prevVal, 1.0],
        "gradient": {
            "start": prevColor,
            "end": USERINPUT_BaseGradient["end"]
        }
    })
    # Get colorised indicator image
    I_c = COLORISERS_THRESHOLDING["Ranged Gradients"](I, intervals=Intervals)
    
    return I_c

# UI Functions
def UI_UploadGreyImage():
    USERINPUT_ImageData = st.file_uploader("Upload Greyscale Image", ['png', 'jpg', 'jpeg', 'bmp'])
    if USERINPUT_ImageData is not None:
        USERINPUT_ImageData = USERINPUT_ImageData.read()
    else:
        USERINPUT_ImageData = open(DEFAULT_PATH_EXAMPLEIMAGE, 'rb').read()
    USERINPUT_gImage = cv2.imdecode(np.frombuffer(USERINPUT_ImageData, np.uint8), cv2.IMREAD_GRAYSCALE)
    st.image(USERINPUT_gImage, caption="Input Image")

    return USERINPUT_gImage

def UI_Coloriser():
    USERINPUT_IntervalCount = st.slider("Interval Count", 2, 10, step=1, value=5)
    col1, indIcol = st.columns(2)
    USERINPUT_BaseGradient = {
        "start": list(Hex_to_RGB(col1.color_picker("Select Base Gradient Start", value=RGB_to_Hex(DEFAULT_COLORISER_BASEGRADIENT["start"]))).astype(np.float32)),
        "end": list(Hex_to_RGB(col1.color_picker("Select Base Gradient End", value=RGB_to_Hex(DEFAULT_COLORISER_BASEGRADIENT["end"]))))
    }
    USERINPUT_Thresholds = []
    USERINPUT_ThresholdColors = []
    for i in range(USERINPUT_IntervalCount-1):
        col1, col2 = st.columns(2)
        color = list(Hex_to_RGB(col1.color_picker("Color #" + str(i+1), value=RGB_to_Hex(DEFAULT_COLORISER_COLORS[i % len(DEFAULT_COLORISER_COLORS)]))))
        th = col2.slider("Threshold #" + str(i+1), 0.0, 1.0, DEFAULT_COLORISER_THRESHOLDS[i % len(DEFAULT_COLORISER_THRESHOLDS)], 0.05)
        USERINPUT_Thresholds.append(th)
        USERINPUT_ThresholdColors.append(color)
    
    I_IndicatorColorised = GenerateColoriserIndicatorImage_Thresholding(USERINPUT_BaseGradient, USERINPUT_Thresholds, USERINPUT_ThresholdColors)
    indIcol.image(I_IndicatorColorised, caption="Coloriser Indicator Image", use_column_width=False)

    return USERINPUT_BaseGradient, USERINPUT_Thresholds, USERINPUT_ThresholdColors

# Repo Based Functions
def threshold_based_coloriser():
    # Title
    st.header("Threshold Based Coloriser")

    # Load Inputs
    USERINPUT_Ig = UI_UploadGreyImage()

    st.write("## Colouring Parameters")
    USERINPUT_BaseGradient, USERINPUT_Thresholds, USERINPUT_ThresholdColors = UI_Coloriser()

    # Process Inputs and Display Outputs
    if st.button("Colorise"):
        USERINPUT_Ig = np.array(USERINPUT_Ig) / 255.0
        I_Color = GenerateColorisedImage_Thresholding(USERINPUT_Ig, USERINPUT_BaseGradient, USERINPUT_Thresholds, USERINPUT_ThresholdColors)
        st.image(I_Color, caption="Colorised Image")
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()