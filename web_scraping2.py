"""
Title: Web Scraping Data from My Drama List - v2
@author: dsherbini
Date Created: January 2025
"""

import pandas as pd
import mechanicalsoup
import streamlit as st
from bs4 import BeautifulSoup



def get_data():
    """
    Logs into and retrieves data from My Drama List website.

    Returns
    -------
    BeautifulSoup object containing My Drama List page content.
    """
    try:
        # Create a browser session
        browser = mechanicalsoup.StatefulBrowser()
        browser.set_user_agent("Mozilla/5.0")

        # Open the login page
        login_url = 'https://mydramalist.com/signin'
        browser.open(login_url)

        # Ensure secrets exist before attempting login
        if not hasattr(st.secrets, 'mydramalist'):
            raise ValueError('MyDramaList credentials not found in Streamlit secrets.')

        # Select and fill the login form
        browser.select_form('form[action="/signin"]')  
        browser['username'] = st.secrets.mydramalist.username
        browser['password'] = st.secrets.mydramalist.password
        browser.submit_selected()

        # Navigate to the desired page after login
        page_url = 'https://mydramalist.com/dramalist/Mystic_pub/completed'
        response = browser.open(page_url)

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        return soup

    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return None



def get_titles(soup):
    """
    Extracts list of k-drama titles.
    """
    # select elements from the website with the following class 
    cite_elements = soup.select('td[class^=mdl-style-col-title]')
    
    # get text from within those elements
    titles_list = [element.get_text(strip=True) for element in cite_elements]
    
    # filter out the 'Korean Drama' column
    titles_edit1 = [s.replace('Korean Drama','') for s in titles_list]
    
    # filter out the 'edit' buttons
    final_titles = [s.replace('edit','') for s in titles_edit1]
    
    return final_titles



def get_reviews(soup):
    """
    Extracts list of k-drama reviews.
    """
    # select elements from the website with the following class
    cite_elements_reviews = soup.select('td[class^=mdl-style-col-notes]')
    
    # get text from those elements (i.e. the reviews)
    reviews = [element.get_text(strip=True) for element in cite_elements_reviews]
    
    # only pull actual reviews; don't pull if blank
    final_reviews = [s for s in reviews if s != '']
    return final_reviews



# join titles and reviews into a data frame
def get_dramas():
    """
    Gets soup, titles, and reviews and then converts to DataFrame.
    """
    # get soup, titles, and reviews
    soup = get_data()
    titles = get_titles(soup)
    reviews = get_reviews(soup)
    
    # combine titles and reviews into datafram
    data = pd.DataFrame({'Title':titles,'Review':reviews})
    
    # remove a few movies from the dataframe
    movie1 = data[data['Title'] == '20th Century Girl'].index
    movie2 = data[data['Title'] == 'Love and Leashes'].index
    movie3 = data[data['Title'] == 'Tune in for Love'].index
    data = data.drop([movie1,movie2,movie3])
    
    return data