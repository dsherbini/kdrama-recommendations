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

st.markdown('')
st.markdown('')

# set subtitle for the app
with st.container():
    st.markdown("""
                     <div style="text-align: center;">
                    Looking for a new k-drama to watch? Look no further! </br>
                    K-drama-rama is here to help. Your next favorite k-drama awaits.
                     </div>
                    """, unsafe_allow_html=True)


st.markdown('')
st.markdown('')
st.markdown('')

# set up containers
with st.container():
    col1, col2, col3 = st.columns([2,2,2])
    with col1:
        st.markdown("")
    
    with col2:
        # button linking to the recommendations page
        if st.button('Get Recommendations',type='primary'):
            st.switch_page('recs.py')
    
    with col3:
        st.markdown("")
    

# add a footer to bottom of app page
st.markdown("""
<p style="font-size: 0.8em; text-align: center; position: fixed; bottom: 0; width: 100%;">
© 2025 Danya Sherbini</p>
""", unsafe_allow_html=True)

