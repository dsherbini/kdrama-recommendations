"""
Title: Streamlit App
@author: dsherbini
Date: March 2023
"""

PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

import streamlit as st
import sys
sys.path.append(PATH)
from recommendation_system import kdramas, features, recommend_kdrama

##################################### APP #####################################

# set title for the app
st.title('K-Drama-Rama!')

# set subtitle for the app
st.markdown("<h5 style='text-align: left; '>Looking for a new k-drama to watch? Look no further! Select a k-drama that you have watched and enjoyed from the list below and get recommendations. <br> <br> Your next favorite k-drama awaits &hearts;<br><br></h5>", unsafe_allow_html=True)

# get list of kdrama titles
titles = list(kdramas['Title'].unique())

# add a default option to the title list
titles.insert(0, 'Select a k-drama')

# set default option as first item in titles list
default_selected_index = 0 

# create a dropdown menu for title
selected_title = st.selectbox('Select an k-drama from the list below:', titles, index=default_selected_index)

# create a drop down menu for number of recommendations
n_recommendations = range(1,11)
selected_n = st.selectbox('How many recommendations do you want?', n_recommendations)

# get recommendations for selected title
if selected_title != 'Select a k-drama':
    recommendations = recommend_kdrama(selected_title, features, n=selected_n)

    # display the selected title and its recommendations
    st.write("Recommended K-dramas:")
    for r in recommendations:
        st.write(f' - {r}')

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2024 Danya Sherbini | <a href="https://www.linkedin.com/in/danyasherbini/" target="_blank">LinkedIn</a> | <a href='https://github.com/dsherbini' target="_blank">GitHub</a>
</p>
""", unsafe_allow_html=True)