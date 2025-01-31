#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recommendations
Created March 2023
Updated Jan 28, 2025
@author: danyasherbini
"""

import pandas as pd
import streamlit as st
from utils.recommendation_system import recommend_kdrama


####################################### DATA ######################################

# load data
@st.cache_data
def load_data():
    df = pd.read_csv('/Users/danyasherbini/Documents/GitHub/kdrama-recommendations/utils/data/kdrama_data_with_features.csv')
    return df

kdramas_final = load_data()


# data cleaning
def process_features(df):
    # drop review columns from the df
    df = df.drop(['Link','Review','Reviews_Clean'],axis = 1)

    # fill NaNs with the general polarity scores for all continuous feature columns
    df = df.apply(lambda row: row.fillna(row['Polarity_Score']), axis=1)

    # for features df, set index as title
    features = df.copy()
    features.set_index('Title', inplace=True)
    
    return features

features = process_features(kdramas_final)



###################################### CSS #######################################

# Custom CSS to change the colors of hyperlinks

# Match colors from config.toml
text_color = '#074799' # text color in config.toml
hover_color = '#7BD3EA' # primary color in config.toml

st.markdown(f"""
    <style>
        /* Make the links use the primary color with !important */
        a {{
            color: {text_color} !important;  /* Primary color from config.toml */
            text-decoration: none !important;  /* Remove underline */
        }}
        a:hover {{
            color: {hover_color} !important;  /* Hover color from config.toml */
        }}
    </style>
""", unsafe_allow_html=True)




################################### PAGE SET UP ###################################
# set title for the app
st.title('Get k-drama recommendations')

# set subtitle for the app
st.markdown('Select a k-drama that you have watched and enjoyed from the list below and get recommendations.')

# get list of kdrama titles
titles = list(kdramas_final['Title'].unique())

# add a default option to the title list
titles.insert(0, 'Select a k-drama')

# set default option as first item in titles list
default_selected_index = 0 

# create a dropdown menu for title
selected_title = st.selectbox('Select a k-drama from the list below:', titles, index=default_selected_index)

# create a drop down menu for number of recommendations
n_recommendations = range(1,11)
selected_n = st.selectbox('How many recommendations do you want?', n_recommendations)

# get recommendations for selected title
if selected_title != 'Select a k-drama':
    recommendations = recommend_kdrama(selected_title, features, n=selected_n)

    # display the selected title and its recommendations
    st.write("Recommended K-dramas:")
    for r in recommendations:
        # Get the corresponding link for each recommendation
        link = kdramas_final[kdramas_final['Title'] == r]['Link'].values
        if link:  # Check if the link exists
            st.markdown(f' - [{r}]({link[0]})')  # Display title as a clickable link
        else:
            st.write(f' - {r}')  # Display title without link if no link exists

    
    

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini</p>
""", unsafe_allow_html=True)
