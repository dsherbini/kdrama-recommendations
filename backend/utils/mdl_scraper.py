#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
My Drama List Scraper v2.0
Created on Wed Jan 29, 2025
@author: danyasherbini

This script scrapes data from a completed watchlist on mydramalist (titles, reviews, images, ratings, etc.)
"""

import os
import pandas as pd
import numpy as np
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import date


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

# Navigate to completed dramas page -- WITH NOTES
driver.get("https://mydramalist.com/dramalist/Mystic_pub/completed?notes=1")
time.sleep(60)  # Wait for JavaScript to load
if "notes" in driver.current_url.lower(): # Check for success
    print("Login successful!")
else:
    print("Login failed.")

# Get soup for page with notes
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

# Navigate to completed dramas page --  WITHOUT NOTES
driver.get("https://mydramalist.com/dramalist/Mystic_pub/completed")
time.sleep(120)  # Wait for JavaScript to load
if driver.current_url.endswith("completed"): # Check for success
    print("Login successful!")
else:
    print("Login failed.")

# Get soup for page without notes
soup2 = BeautifulSoup(driver.page_source, "html.parser")

# Extract year
def get_years(soup):
    cite_elements_years = soup.select('td[class^=mdl-style-col-year]')
    years = [element.get_text(strip=True) for element in cite_elements_years if element.get_text(strip=True)]
    return years 

years = get_years(soup2)

# Extract my personal rating for each drama
def get_my_ratings(soup):
    cite_elements_scores = soup.select('td[class^=mdl-style-col-score]')
    my_ratings = [element.get_text(strip=True) for element in cite_elements_scores if element.get_text(strip=True)]
    return my_ratings

my_ratings = get_my_ratings(soup2)

# Extract data from the popover that appears when hovering over a drama title
def get_popover_data(ids):
    korean_original_titles = []
    translated_original_titles = []
    image_urls = []
    scores = []
    synopses = []
    genres_list = []
    skipped_drama_ids = []  # List to keep track of any dramas that are skipped over as the scraper runs


    for drama_id in ids:
        
        try: 
            # For each drama in the list, locate the drama in the table on the page
            locate_drama = driver.find_element(By.CSS_SELECTOR, f"#ml{drama_id} > td.mdl-style-col-title.sort1 > a")

            # Use ActionChains to hover over the element in order for the popover to appear
            actions = ActionChains(driver)
            actions.move_to_element(locate_drama).perform()

            # Wait for popover to appear
            time.sleep(2) 

            WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"#qtip-{drama_id}-title-content"))
            )

            # Scrape the popover content
            popover = driver.find_element(By.CSS_SELECTOR, f"#qtip-{drama_id}-title-content") 

            # Extract original Korean title and clean
            try: 
                korean_title = popover.find_element(By.CSS_SELECTOR, ".original-title").text
                if " (Korean Drama)" in korean_title:
                    korean_title = korean_title.replace(" (Korean Drama)", "")
            except: 
                korean_title = 'Original Title Unavailable'

            # Extract translated English version of Korean title and clean
            try: 
                # Get url slug from popover
                drama_slug = popover.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href").split("/")[-1]  # Extracts the last part of the URL
                
                # Remove hyphens, numbers, and capitalize each word
                clean_slug = ''.join([char for char in drama_slug if not char.isdigit()]).lstrip("-").replace("-", " ").title()
            except: 
                clean_slug = 'Translation Unavailable'

            # Extract image
            try:
                image_url = popover.find_element(By.TAG_NAME, "img").get_attribute("src")
            except: 
                image_url = 'Image Unavailable'
            
            # Extract my drama list rating
            try:
                score = popover.find_element(By.CLASS_NAME, "score").text
            except: 
                score = 'Rating Unavailable'
            
            # Extract synopsis
            try:
                synopsis = popover.find_element(By.CLASS_NAME, "synopsis").text
            except:
                synopsis = 'Synopsis Unavailable'

            # Extract list of genre tags for each drama
            try: 
                # Find all individual genre tags within the .genre-tags container, which are <a> tags
                genre_elements = popover.find_elements(By.CSS_SELECTOR, ".genre-tags a")
    
                # Extract the text of each <a> tag and store them in a list
                genres = [genre.text for genre in genre_elements]
            except:
                genres = ['Genre Unavailable']

            # Append data to lists
            korean_original_titles.append(korean_title)
            translated_original_titles.append(clean_slug)
            image_urls.append(image_url)
            scores.append(score)
            synopses.append(synopsis)
            genres_list.append(genres) # this is a list of lists

        except TimeoutException:
            print(f"Popover not found for drama ID {drama_id}, skipping...")
            skipped_drama_ids.append(drama_id)  # Append the skipped drama ID to the list
            continue  # Skip this drama and continue with the next one

    return korean_original_titles, translated_original_titles, image_urls, scores, synopses, genres_list, skipped_drama_ids

# Get popover data
korean_original_titles, translated_original_titles, image_urls, scores, synopses, genres_list, skipped_drama_ids = get_popover_data(ids)

# Re-scrape any skipped-over dramas individually
def get_single_drama_popover(drama_id):
    """
    Returns popover data for a single drama ID
    """
    try:
        locate_drama = driver.find_element(By.CSS_SELECTOR, f"#ml{drama_id} > td.mdl-style-col-title.sort1 > a")
        actions = ActionChains(driver)
        actions.move_to_element(locate_drama).perform()
        time.sleep(2)

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"#qtip-{drama_id}-title-content"))
        )

        popover = driver.find_element(By.CSS_SELECTOR, f"#qtip-{drama_id}-title-content")

        # Extract fields
        try: korean_title = popover.find_element(By.CSS_SELECTOR, ".original-title").text.replace(" (Korean Drama)", "")
        except: korean_title = "Original Title Unavailable"

        try:
            drama_slug = popover.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href").split("/")[-1]
            translated_title = ''.join([c for c in drama_slug if not c.isdigit()]).lstrip("-").replace("-", " ").title()
        except:
            translated_title = "Translation Unavailable"

        try: image_url = popover.find_element(By.TAG_NAME, "img").get_attribute("src")
        except: image_url = "Image Unavailable"

        try: score = popover.find_element(By.CLASS_NAME, "score").text
        except: score = "Rating Unavailable"

        try: synopsis = popover.find_element(By.CLASS_NAME, "synopsis").text
        except: synopsis = "Synopsis Unavailable"

        try:
            genres = [g.text for g in popover.find_elements(By.CSS_SELECTOR, ".genre-tags a")]
        except:
            genres = ["Genre Unavailable"]

        return korean_title, translated_title, image_url, score, synopsis, genres

    except Exception as e:
        print(f"Failed to scrape drama {drama_id}: {e}")
        return None, None, None, None, None, None

def grab_and_insert_one_drama(kdrama_id):
    """
    Grabs data for one drama and inserts it into the correct position in the list
    """

    # Get popover data for individual drama
    og_title, trans_title, img_url, indv_score, indv_synopsis, indv_genres = get_single_drama_popover(kdrama_id)
    
    # If title is not found, skip this drama
    if og_title is None:
        print(f"Skipping drama {kdrama_id} because data was not found.")
        return

    # Get position / order of the drama from the original ids list
    position = ids.index(kdrama_id)

    # Insert data into each data list
    korean_original_titles.insert(position, og_title)
    translated_original_titles.insert(position, trans_title)
    image_urls.insert(position, img_url)
    scores.insert(position, indv_score)
    synopses.insert(position, indv_synopsis)
    genres_list.insert(position, indv_genres)

# Loop through skipped drama IDs and re-scrape them
for drama_id in skipped_drama_ids:
    grab_and_insert_one_drama(drama_id)


# Print output
print(korean_original_titles)
print(translated_original_titles)
print(image_urls)
print(scores)
print(synopses)
print(genres_list)

# Combine Data
def get_dramas(titles, korean_original_titles, translated_original_titles, years, links, my_ratings, reviews, image_urls, scores, synopses, genres_list):
    data = pd.DataFrame({
        'Title': titles,
        'Korean Title': korean_original_titles,
        'Translated Title': translated_original_titles,
        'Year': years,
        'Link': links,
        'Review': reviews,
        'Rating': my_ratings,
        'Image': image_urls,
        'Score': scores,
        'Synopsis': synopses,
        'Genres': genres_list
    })

    # drop movies
    data = data[~data["Korean Title"].str.contains("Movie", case=False, na=False)]

    return data

my_data = get_dramas(titles, korean_original_titles, translated_original_titles, years, links, my_ratings, reviews, image_urls, scores, synopses, genres_list)
print(my_data.head())
print(len(my_data))

# View drama details by title
def get_drama_by_title(title, df):
    """
    Returns the row in the DataFrame for a given drama title.
    title: string (exact title or part of it)
    df: your scraped DataFrame (my_data)
    """
    # Case-insensitive search
    result = df[df['Title'].str.lower() == title.lower()]
    
    if result.empty:
        return f"No drama found with title '{title}'"
    else:
        return result.to_dict(orient='records')[0]
    
title = "A Virtuous Business"
details = get_drama_by_title(title, my_data)
print(details)

# Save all data as CSV
today = date.today() # get today's date for file name
output_dir = './data' # save to this folder
os.makedirs(output_dir, exist_ok=True) # make the folder if it doesn't already exist
output_path = os.path.join(output_dir, f"scraped_data_img_{today}.csv") # filename
my_data.to_csv(output_path, index=False, encoding='utf-8') # save data as csv file
print(f"File saved successfully at {output_path}")

# Close the browser
driver.quit()

