#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Welcome/Landing Page
Created Jan 28, 2025
@author: danyasherbini
"""

import streamlit as st

# set title for the app
st.title('Find your next favorite k-drama.')

# set subtitle for the app
st.markdown('##### Looking for a new k-drama to watch? Look no further! Kdramarama is here to help.')
st.markdown('##### Your next favorite k-drama awaits.')
st.markdown('')
st.markdown('')
st.markdown('')



col1, col2, col3 = st.columns([3,3,3])
with col1:
    st.markdown("")

with col2:
    # link to recs page
    with st.container():
        st.page_link('recs.py',label='Get recommendations.', use_container_width=True)

with col3:
    st.markdown("")
    

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini</p>
""", unsafe_allow_html=True)
