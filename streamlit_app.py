"""
Title: Streamlit App
@author: dsherbini
Date: March 2023
"""

PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(PATH)
from recommendation_system import kdramas, features, recommend_kdrama

##################################### APP #####################################

# get list of kdrama titles
titles = kdramas['Title'].unique()

# create a dropdown menu
selected_title = st.selectbox('Select an K-Drama that you have watched before and enjoyed:', titles)

# get recommendations for selected option
recommendations = recommend_kdrama(selected_title, features)

for r in recommendations:
    st.write(f'Recommended K-drama: {r}')

