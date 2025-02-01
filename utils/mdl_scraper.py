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
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# Load credentials from secrets
username = st.secrets["mydramalist"]["username"]
password = st.secrets["mydramalist"]["password"]

# Set up selenium webdriver
options = webdriver.ChromeOptions()
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

# Load credentials from secrets
username = st.secrets["mydramalist"]["username"]
password = st.secrets["mydramalist"]["password"]

# Enter email
email_input = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div/div/form/div[2]/input')
email_input.send_keys(username)

# Enter password
password_input = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[2]/div[1]/div/div/form/div[3]/input')
password_input.send_keys(password)

# Press Enter to log in
password_input.send_keys(Keys.RETURN)  
time.sleep(120)  # Wait for login to complete -- takes a while bc the main page has a lot of ads/images

# Check if login was successful
if "signin" in driver.current_url.lower():
    print("Login failed. Check credentials or solve CAPTCHA manually.")
    driver.quit()
else:
    print("Login successful!")

# Navigate to completed dramas page -- with notes
driver.get("https://mydramalist.com/dramalist/Mystic_pub/completed?notes=1")
time.sleep(60)  # Wait for JavaScript to load
if "notes" in driver.current_url.lower(): # Check for success
    print("Login successful!")
else:
    print("Login failed.")

# Get soup
soup1 = BeautifulSoup(driver.page_source, "html.parser")

# Extract Titles
def get_titles(soup):
    cite_elements = soup.select('[class^=mdl-style-col-title]')
    titles_list = [element.get_text(strip=True).replace('Korean Drama', '').replace('edit', '') for element in cite_elements]
    return titles_list

titles = get_titles(soup1)

# Extract Hyperlinks
def get_links(soup):
    link_elements = soup.select('[class^=mdl-style-col-title] a.title.text-primary')
    links_list = [f"https://mydramalist.com/{element['href'].lstrip('/')}" for element in link_elements if 'href' in element.attrs]
    return links_list

links = get_links(soup1)

# Extract IDs from URLs (last part of hyperlink)
ids = [link.split("/")[-1].split("-")[0] for link in links]

# Extract my reviews
def get_reviews(soup):
    cite_elements_reviews = soup.select('td[class^=mdl-style-col-notes]')
    reviews = [element.get_text(strip=True) for element in cite_elements_reviews if element.get_text(strip=True)]
    return reviews

reviews = get_reviews(soup1)

# Navigate to completed dramas page -- without notes
driver.get("https://mydramalist.com/dramalist/Mystic_pub/completed")
time.sleep(120)  # Wait for JavaScript to load
if driver.current_url.endswith("completed"): # Check for success
    print("Login successful!")
else:
    print("Login failed.")

# Get soup
soup2 = BeautifulSoup(driver.page_source, "html.parser")

# Extract image, score, and synopsis from the popover that appears when hovering over a drama title
def get_popover_data(ids):
    image_urls = []
    scores = []
    synopses = []

    for drama_id in ids:
        # For each drama in the list, locate the drama in the table on the page
        locate_drama = driver.find_element(By.CSS_SELECTOR, f"#ml{drama_id} > td.mdl-style-col-title.sort1 > a")

        # Use ActionChains to hover over the element in order for the popover to appear
        actions = ActionChains(driver)
        actions.move_to_element(locate_drama).perform()

        # Wait for popover to appear
        time.sleep(2) 

        # Scrape the popover content
        popover = driver.find_element(By.CSS_SELECTOR, f"#qtip-{drama_id}-title-content") 

        # Extract image, score, and synopsis
        image_url = popover.find_element(By.TAG_NAME, "img").get_attribute("src")
        score = popover.find_element(By.CLASS_NAME, "score").text
        synopsis = popover.find_element(By.CLASS_NAME, "synopsis").text

        image_urls.append(image_url)
        scores.append(score)
        synopses.append(synopsis)

    return image_urls, scores, synopses

# Get popover data
image_urls, scores, synopses = get_popover_data(ids)

# print output
print(image_urls)
print(scores)
print(synopses)

# Combine Data
def get_dramas(titles, links, reviews, image_urls, scores, synopses):
    data = pd.DataFrame({
        'Title': titles,
        'Link': links,
        'Review': reviews,
        'Image': image_urls,
        'Score': scores,
        'Synopsis': synopses
    })
    return data

my_data = get_dramas(titles, links, reviews, image_urls, scores, synopses)
print(my_data.head())

# Save as CSV
output_dir = './data'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'scraped_data_img.csv')
my_data.to_csv(output_path, index=False, encoding='utf-8')
print(f"File saved successfully at {output_path}")

# Close the browser
driver.quit()





#####################################################################################################
# sandbox

# Testing out code to get popover data with one title

# Find the element that triggers the popover (e.g., a show title)
locate_drama = driver.find_element(By.CSS_SELECTOR, "#ml729303 > td.mdl-style-col-title.sort1 > a")

# Use ActionChains to hover over the element
actions = ActionChains(driver)
actions.move_to_element(locate_drama).perform()

# Wait for popover to appear
time.sleep(2)

# Scrape the popover content
popover = driver.find_element(By.CSS_SELECTOR, "#qtip-729303-title-content") 

# Extract image, score, and synopsis
image_url = popover.find_element(By.TAG_NAME, "img").get_attribute("src")
score = popover.find_element(By.CLASS_NAME, "score").text
synopsis = popover.find_element(By.CLASS_NAME, "synopsis").text

# Print results
print("Image URL:", image_url)
print("Score:", score)
print("Synopsis:", synopsis)

