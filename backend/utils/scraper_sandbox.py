# sandbox
## scratch file for testing out web scraping code

# Getting popover data for soudtrack #1: id # is 713865
soundtrack_id = ['713865']
soundtrack_original_title, soundtrack_translated_original_title, soundtrack_image_url, soundtrack_score, soundtrack_synopsis, soundtrack_genres_list = get_popover_data(soundtrack_id)
korean_original_titles.insert(104, soundtrack_original_title)
translated_original_titles.insert(104, soundtrack_translated_original_title)
image_urls.insert(104,soundtrack_image_url)
scores.insert(104,soundtrack_score)
synopses.insert(104,soundtrack_synopsis)
genres_list.insert(104,soundtrack_genres_list)


print(ids[104])
my_data.iloc['Something in the Rain']
translated_original_titles[104]
ids.index('713865')

# Testing out code to get popover data with one title

# Find the element that triggers the popover (e.g., a show title)
locate_drama_test = driver.find_element(By.CSS_SELECTOR, "#ml729303 > td.mdl-style-col-title.sort1 > a")

# Use ActionChains to hover over the element
actions = ActionChains(driver)
actions.move_to_element(locate_drama_test).perform()

# Wait for popover to appear
time.sleep(2)

# Scrape the popover content
popover_test = driver.find_element(By.CSS_SELECTOR, "#qtip-729303-title-content") 

# Get translation of original title
drama_slug = popover_test.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href").split("/")[-1]  # Extracts the last part of the URL
# Remove the hyphen and capitalize each word
clean_slug = ''.join([char for char in drama_slug if not char.isdigit()]).lstrip("-").replace("-", " ").title()
print(clean_slug)

 # If it exists, extract original title and clean
original_title_test = popover_test.find_element(By.CSS_SELECTOR, ".original-title").text
if " (Korean Drama)" in original_title_test:
    original_title_test = original_title_test.replace(" (Korean Drama)", "")

print(original_title_test)


# Find all individual genre tags within the .genre-tags container, which are <a> tags
genre_elements = popover_test.find_elements(By.CSS_SELECTOR, ".genre-tags a")
    
# Extract the text of each <a> tag and store them in a list
genres_test = [genre.text for genre in genre_elements]

print(genres_test)

# Extract image, score, and synopsis
image_url = popover.find_element(By.TAG_NAME, "img").get_attribute("src")
score = popover.find_element(By.CLASS_NAME, "score").text
synopsis = popover.find_element(By.CLASS_NAME, "synopsis").text

# Print results
print("Image URL:", image_url)
print("Score:", score)
print("Synopsis:", synopsis)

