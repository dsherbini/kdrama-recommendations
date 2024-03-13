"""
Title: Streamlit App
@author: dsherbini
Date: March 2023
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

# import k-drama data
kdramas = pd.read_csv(os.path.join(PATH, 'kdrama_data_with_features'))

################################ DATA CLEANING ################################

# drop review columns from the df
kdramas = kdramas.drop(['Review','Reviews_Clean'],axis = 1)

# fill NaNs with the general polarity scores for all continuous feature columns
kdramas = kdramas.apply(lambda row: row.fillna(row['Polarity_Score']), axis=1)

# for features df, set index as title
features = kdramas.copy()
features.set_index('Title', inplace=True)


##################################### APP #####################################

# Get the unique values from the column you want to use for the dropdown
options = kdramas['Title'].unique()

# Create the dropdown menu
selected_option = st.selectbox('Select an option:', options)

# Display the selected option
st.write(f'You selected: {selected_option}')
