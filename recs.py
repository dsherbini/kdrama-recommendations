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

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/kdrama_data_with_features.csv')
    return df

kdramas_final = load_data()

# Data cleaning
def process_features(df):
    # drop review columns from the df
    cols_to_drop = ['Review','Link','Image','Score','Synopsis','Reviews_Clean']
    df = df.drop(cols_to_drop,axis = 1)

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
selected_title = st.selectbox('Get recommendations for:', titles, index=default_selected_index)

# create a drop down menu for number of recommendations
n_recommendations = list(range(1,6))
n_recommendations.insert(0, 'Select number of recommendations') # add a default option to the n_recs list
selected_n = st.selectbox('How many recommendations do you want?', n_recommendations)

# get recommendations for selected title
if selected_title != 'Select a k-drama':
    recommendations = recommend_kdrama(selected_title, features, n=selected_n)

    # display the selected title and its recommendations
    st.write("Recommended K-dramas:")
    for r in recommendations:
        # Show details for each recommendation
        rec_data = kdramas_final[kdramas_final['Title'] == r]
        if not rec_data.empty:
            link = rec_data['Link'].values[0] if 'Link' in rec_data else None
            image = rec_data['Image'].values[0] if 'Image' in rec_data else None
            score = rec_data['Score'].values[0] if 'Score' in rec_data else "N/A"
            synopsis = rec_data['Synopsis'].values[0] if 'Synopsis' in rec_data else "Synopsis not available."

            # Display title as an expander
            with st.expander(f"**{r}**"):
                if image:
                    st.image(image, width=100)  # Show image
                if link:
                    st.markdown(f"[📺 Get more details]({link})")  # Show link
                st.write(f"**⭐ MyDramaList Rating:** {score}")
                st.write(f"**📖 Synopsis:** {synopsis}")
        #else:
            #st.write(f" - {r}")  # If no data found, just display title

# optional -- do something if they don't select both title and n_recommendations        
#elif selected_title == 'Select a k-drama':
#    st.write('')
#    st.write('')
#    st.write('Please select a k-drama from the list above to get recommendations.')
    
    

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini</p>
""", unsafe_allow_html=True)
