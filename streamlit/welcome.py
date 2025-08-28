#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Welcome/Landing Page
Created Jan 28, 2025
@author: danyasherbini
"""

import streamlit as st

# Set title for the app
st.markdown("<h1 style='text-align: center;'>Find your next favorite k-drama.</h1>", unsafe_allow_html=True)
st.markdown('')
st.markdown('')

# Set subtitle for the app
with st.container():
    col1,col2,col3 = st.columns([1,1,1])
    
    with col1:
        st.markdown('')
    
    with col2:
        st.markdown("<p style='text-align: center;'>Looking for a new k-drama to watch? Look no further! K-drama-rama is here to help. Your next favorite k-drama awaits.</p>", unsafe_allow_html=True)

    with col3: 
        st.markdown('')
        st.markdown('')  

st.markdown('')
st.markdown('') 

# Center the button using custom HTML & CSS
st.markdown(
    """
    <style>
    .stButton > button {
        display: block;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Button that links to the recommendations page
if st.button('Get recommendations!', type='primary'):
    st.switch_page('recs.py')



