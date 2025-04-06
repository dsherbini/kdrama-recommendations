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
    df = pd.read_csv('utils/data/kdrama_data_with_features.csv')
    return df

kdramas_final = load_data()

# Data cleaning
def process_features(df):
    # drop review columns from the df
    cols_to_drop = ['Review','Link','Image','Score','Synopsis','Reviews_Clean', 'Korean Title', 'Translated Title','Year','Rating','Genres']
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
st.markdown("<h1 style='text-align: center;'>Get k-drama recommendations.</h1>", unsafe_allow_html=True)
st.markdown('')
st.markdown('')

# set subtitle for the app
with st.container():
    col1,col2,col3 = st.columns([2,5,2])
    
    with col1:
        st.markdown('')
    
    with col2:
        st.markdown("<p style='text-align: center;'>Select a k-drama that you have watched and enjoyed from the list below and get recommendations.</p>", unsafe_allow_html=True)

    with col3: 
        st.markdown('')
        st.markdown('')  

# get list of kdrama titles
titles = list(kdramas_final['Title'].unique())

# Create a layout with three columns (side-empty, centered, side-empty)
with st.container():
    col1, col2, col3 = st.columns([1, 2.5, 1])  
    with col1:
        st.empty()

    with col2:  # Center column
        # create a dropdown menu for title
        selected_title = st.selectbox('', titles,index=None,placeholder='Select a k-drama')

        # create a drop down menu for number of recommendations
        n_recommendations = range(1,6)
        selected_n = st.selectbox('', n_recommendations,index=None,placeholder='Select number of recommendations')

    with col3:
        st.empty()

st.markdown('')
st.markdown('')
st.markdown('')


with st.container():
    col1,col2,col3 = st.columns([1,2.5,1])
    
    with col1:
        st.empty()
    
    with col2:
        # get recommendations for selected title
        if selected_title != None and selected_n != None:
            recommendations = recommend_kdrama(selected_title, features, n=selected_n)

            # display the selected title and its recommendations
            st.markdown("#### Recommended k-dramas:")
            for r in recommendations:
                # Show details for each recommendation
                rec_data = kdramas_final[kdramas_final['Title'] == r]
                if not rec_data.empty:
                    korean_title = rec_data['Korean Title'].values[0] if 'Korean Title' in rec_data else None
                    translated_title = rec_data['Translated Title'].values[0] if rec_data['Translated Title'].values[0] != rec_data['Title'].values[0] else None
                    link = rec_data['Link'].values[0] if 'Link' in rec_data else None
                    image = rec_data['Image'].values[0] if 'Image' in rec_data else None
                    #score = rec_data['Score'].values[0] if 'Score' in rec_data else None
                    rating = rec_data['Rating'].values[0] if 'Rating' in rec_data else None
                    synopsis = rec_data['Synopsis'].values[0] if 'Synopsis' in rec_data else None
                    genres = rec_data['Genres'].values[0] if 'Genres' in rec_data else None

                    # Display title as an expander
                    with st.expander(f"**{r}**"):
                        with st.container():
                            col1,col2 = st.columns([3,10]) 
                            with col1:
                                if image:
                                    st.image(image, width=100)  # Show image
                            with col2:
                                if korean_title is not None:
                                    st.markdown(f"**🇰🇷 Original Korean Title:** {korean_title}") 
                                
                                if translated_title is not None:
                                    st.markdown(f"**🔄 Translated Original Title:** {translated_title}")
                
                                if rating is not None:
                                    st.write(f"**⭐ Rating:** {rating}")
                                
                                if genres is not None:
                                    st.markdown(f"**🎭 Genres:** {genres}")

                                if link is not None:
                                    st.markdown(f"**📺 [Get more details]({link})**")
                                st.markdown('')
                        
                        if synopsis is not None:
                            st.write(f"**📖 Synopsis:** {synopsis}")
                #else:
                    #st.write(f" - {r}")  # If no data found, just display title

        # optional -- do something if they don't select both title and n_recommendations        
        #elif selected_title == 'Select a k-drama':
        #    st.write('')
        #    st.write('')
        #    st.write('Please select a k-drama from the list above to get recommendations.')
    
    
    with col3:
        st.empty()

    


