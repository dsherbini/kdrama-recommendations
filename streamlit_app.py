"""
Title: Kdramarama
@author: dsherbini
Created: March 2023
"""

import streamlit as st

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

# Pages
welcome = st.Page('welcome.py',title='Welcome',icon='✨')
recs = st.Page('recs.py', title='Recommendations', icon='✨')

# Build navigation bar
pg = st.navigation([welcome,recs],expanded=False)

# Add logo
#logo = './assets/logo.png'

#st.logo(
#    logo,
#    link="https://techequity.us"
#)

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini</p>
""", unsafe_allow_html=True)

# Run the pages
pg.run()





