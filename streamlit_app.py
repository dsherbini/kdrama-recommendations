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

# store all recommendations in a dataframe
recommendations = {}
for title in titles:
    reccos = recommend_kdrama(title, features)
    recommendations.keys().append(title)
    recommendations.values().append(reccos)
    recommendations_df = pd.DataFrame(recommendations, columns = ['Title', 'Recommendations']


# create a dropdown menu
selected_title = st.selectbox('Select an K-Drama that you have watched before and enjoyed:', titles)

# get recommendations for selected option
recommendations = recommend_kdrama(selected_title, features)

if recommendations is None:
    st.write("No recommendations found.")
else:
    for r in recommendations:
        st.write(f'Recommended K-drama: {r}')


recommend_kdrama('My Mister',features,5)
