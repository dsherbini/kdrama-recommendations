#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Welcome/Landing Page
Created Jan 28, 2025
@author: danyasherbini
"""

import streamlit as st

# set title for the app
st.title('Find your next K-drama')

# set subtitle for the app
st.markdown("<h5 style='text-align: left; '>Looking for a new k-drama to watch? Look no further! Select a k-drama that you have watched and enjoyed from the list below and get recommendations. <br> <br> Your next favorite k-drama awaits &hearts;<br><br></h5>", unsafe_allow_html=True)

st.page_link('recs.py',label='Find your next favorite k-drama.')

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini</p>
""", unsafe_allow_html=True)
