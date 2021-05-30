"""
Stream lit GUI for hosting ImageColoriser
"""

# Imports
import cv2
import numpy as np
import streamlit as st
import json

import ImageColoriser

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
DEFAULT_PATH_EXAMPLEIMAGE = 'Examples/Staircase.png'

COLORISERINDICATORIMAGE_SIZE = [128, 128]
DEFAULT_COLORISER_BASECOLOR = [65, 105, 225]
DEFAULT_COLORISER_THRESHOLDS = [0.25, 0.6, 0.85, 0.95]
DEFAULT_COLORISER_COLORS = [[238, 214, 175], [34, 139, 34], [139, 137, 137], [255, 250, 250]]

RADIALINDICATORIMAGE = None

# Util Functions
def Hex_to_RGB(val):
    val = val.lstrip('#')
    lv = len(val)
    return tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def RGB_to_Hex(rgb):
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
def GenerateColoriserIndicatorImage(USERINPUT_BaseColor, USERINPUT_Thresholds, USERINPUT_ThresholdColors):
    RADIALINDICATORIMAGE = GenerateRadialIndicatorImage()
    # Apply Thresholds and Colors
    I_ic = ImageColoriser.ImageColoriser_Thresholding.ColoriseImage_ThresholdingSimple(I=RADIALINDICATORIMAGE, thresholds=USERINPUT_Thresholds, thresholdColors=USERINPUT_ThresholdColors, defaultColor=USERINPUT_BaseColor)
    return I_ic

# Main Functions
@st.cache
def ThresholdColoriser(USERINPUT_gImage, USERINPUT_BaseColor, USERINPUT_Thresholds, USERINPUT_ThresholdColors):
    I_g = np.array(USERINPUT_gImage, dtype=float) / 255
    I_c = ImageColoriser.ImageColoriser_Thresholding.ColoriseImage_ThresholdingSimple(I=I_g, thresholds=USERINPUT_Thresholds, thresholdColors=USERINPUT_ThresholdColors, defaultColor=USERINPUT_BaseColor)
    return I_c

# UI Functions
def UI_UploadGreyImage():
    USERINPUT_ImageData = st.file_uploader("Upload Black and White Image", ['png', 'jpg', 'jpeg', 'bmp'])
    if USERINPUT_ImageData is not None:
        USERINPUT_ImageData = USERINPUT_ImageData.read()
    else:
        USERINPUT_ImageData = open(DEFAULT_PATH_EXAMPLEIMAGE, 'rb').read()
    USERINPUT_gImage = cv2.imdecode(np.frombuffer(USERINPUT_ImageData, np.uint8), cv2.IMREAD_GRAYSCALE)
    st.image(USERINPUT_gImage, caption="Input Image")

    return USERINPUT_gImage

def UI_ClusteringMethod():
    USERINPUT_Method = st.selectbox("Select Mapping Method", ImageColoriser.ImageColoriser_Clustering.MAPPING_METHODS).lower()
    return USERINPUT_Method

def UI_Coloriser():
    USERINPUT_ColorCount = st.slider("Colors", 2, 10, step=1, value=5)
    col1, indIcol = st.beta_columns(2)
    USERINPUT_BaseColor = list(Hex_to_RGB(col1.color_picker("Select Base Color", value=RGB_to_Hex(DEFAULT_COLORISER_BASECOLOR))))
    USERINPUT_Thresholds = []
    USERINPUT_ThresholdColors = []
    for i in range(USERINPUT_ColorCount-1):
        col1, col2 = st.beta_columns(2)
        color = list(Hex_to_RGB(col1.color_picker("Color #" + str(i+1), value=RGB_to_Hex(DEFAULT_COLORISER_COLORS[i % len(DEFAULT_COLORISER_COLORS)]))))
        th = col2.slider("Threshold #" + str(i+1), 0.0, 1.0, DEFAULT_COLORISER_THRESHOLDS[i % len(DEFAULT_COLORISER_THRESHOLDS)], 0.05)
        USERINPUT_Thresholds.append(th)
        USERINPUT_ThresholdColors.append(color)
    
    I_IndicatorColorised = GenerateColoriserIndicatorImage(USERINPUT_BaseColor, USERINPUT_Thresholds, USERINPUT_ThresholdColors)
    indIcol.image(I_IndicatorColorised, caption="Coloriser Indicator Image", use_column_width=False, clamp=True)

    return USERINPUT_BaseColor, USERINPUT_Thresholds, USERINPUT_ThresholdColors

# Repo Based Functions
def clustering_based_coloriser():
    # Title
    st.header("Clustering Based Coloriser")

    # Load Inputs
    USERINPUT_gImage = UI_UploadGreyImage()
    USERINPUT_Method = UI_ClusteringMethod()

    # Process Inputs
    I_Color = ImageColoriser.ImageColoriser_Clustering.ColoriseImage_ClusteringSimple(I=USERINPUT_gImage, method=USERINPUT_Method)

    # Display Outputs
    if st.button("Colorise"):
        st.image(I_Color, caption="Colorised Image")

def threshold_based_coloriser():
    # Title
    st.header("Threshold Based Coloriser")

    # Load Inputs
    USERINPUT_gImage = UI_UploadGreyImage()

    st.write("## Colouring Parameters")
    USERINPUT_BaseColor, USERINPUT_Thresholds, USERINPUT_ThresholdColors = UI_Coloriser()

    # Process Inputs
    I_Color = ThresholdColoriser(USERINPUT_gImage, USERINPUT_BaseColor, USERINPUT_Thresholds, USERINPUT_ThresholdColors)

    # Display Outputs
    if st.button("Colorise"):
        st.image(I_Color, caption="Colorised Image")
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()