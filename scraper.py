#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
My Drama List Scraper v2.0
Created on Wed Jan 29, 2025
@author: danyasherbini
"""
import os
import pandas as pd
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Load credentials from secrets
username = st.secrets["mydramalist"]["username"]
password = st.secrets["mydramalist"]["password"]

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Remove this if you want to see the browser
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open MyDramaList login page
driver.get("https://mydramalist.com/signin")
time.sleep(30)  # Wait for page to load

# Enter email
email_input = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div/div/form/div[2]/input')
email_input.send_keys(username)

# Enter password
password_input = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div/div/form/div[3]/input')
password_input.send_keys(password)

# Press Enter to log in
password_input.send_keys(Keys.RETURN)  
time.sleep(300)  # Wait for login to complete

# Check if login was successful
if "signin" in driver.current_url.lower():
    print("Login failed. Check credentials or solve CAPTCHA manually.")
    driver.quit()
else:
    print("Login successful!")

    # Navigate to a page with dramas (e.g., the homepage or a search result page)
    driver.get("https://mydramalist.com/dramalist/Mystic_pub/completed?notes=1")
    time.sleep(160)  # Wait for JavaScript to load

    # Parse page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(soup.prettify())

    
# Get titles
def get_titles(soup):
    """
    Extracts list of k-drama titles.
    """
    # select elements from the website with the following class 
    cite_elements = soup.select('[class^=mdl-style-col-title]')
    
    # get text from within those elements
    titles_list = [element.get_text(strip=True) for element in cite_elements]
    
    # filter out the 'Korean Drama' column
    titles_edit1 = [s.replace('Korean Drama','') for s in titles_list]
    
    # filter out the 'edit' buttons
    final_titles = [s.replace('edit','') for s in titles_edit1]
    
    return final_titles

titles = get_titles(soup)

# Get hyperlinks
def get_links(soup):
    """
    Extracts list of k-drama links (the part after href) and adds the base URL.
    """
    # Select elements from the website with the following class
    link_elements = soup.select('[class^=mdl-style-col-title] a.title.text-primary')

    # Extract the href attribute if it exists and remove the leading "/"
    links_list = [f"https://mydramalist.com/{element['href'].lstrip('/')}" for element in link_elements if 'href' in element.attrs]

    return links_list

links = get_links(soup)

# Get reviews
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

reviews = get_reviews(soup)

# Join and clean data
def get_dramas(titles, links, reviews):
    """
    Convert titles, links, and reviews to final dataframe.
    """
    # combine titles and reviews into dataframe
    data = pd.DataFrame({'Title':titles,'Link':links,'Review':reviews})
    
    # remove a few movies from the dataframe
    movie1 = data[data['Title'] == '20th Century Girl'].index
    movie2 = data[data['Title'] == 'Love and Leashes'].index
    movie3 = data[data['Title'] == 'Tune in for Love'].index
    data = data.drop(movie1)
    data = data.drop(movie2)
    data = data.drop(movie3)
    
    return data

my_data = get_dramas(titles, links, reviews)

# Save as csv file
output_dir = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations/data'
os.makedirs(output_dir, exist_ok=True)  # ensure directory exists
output_path = os.path.join(output_dir,'scraped_data_2025.01.29.csv')
my_data.to_csv(output_path, index=False, encoding='utf-8')
print(f"File saved successfully at {output_path}")

# Close the browser
driver.quit()    

