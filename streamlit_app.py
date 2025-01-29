"""
Title: Streamlit App
@author: dsherbini
Date: March 2023
"""

import streamlit as st
from recommendation_system import kdramas, features, recommend_kdrama

# page configuration
st.set_page_config(
    page_title='K-Drama-Rama',
    page_icon='✨',
    layout='centered',
    initial_sidebar_state='auto',
    menu_items={
        'Get help': None,
        'Report a bug': 'https://github.com/dsherbini/kdrama-recommendations/issues',
        'About': "Hi, I'm Danya. I made K-Drama-Rama because I love to watch Korean dramas. The recommendations in this app are based on the dramas I've personally watched and my own analysis. For more information on how I generated these recommendations and how I built this app, feel free to check out my [GitHub](https://github.com/dsherbini/kdrama-recommendations)."
    }
)
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
        st.write(f' - {r}')

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini | <a href='https://github.com/dsherbini' target="_blank">GitHub</a>
</p>
""", unsafe_allow_html=True)


