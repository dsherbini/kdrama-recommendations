"""
Title: Web Scraping Data from My Drama List
@author: dsherbini
Date: January 2023
"""

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

###############################################################################

def get_data():
    """
    Retrieves data from My Drama List website. Because the website requires an account login, 
    this function uses cookies and headers converted to python from cURL in order to create the soup.
    Source: https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup
    """
    cookies = {
        'InstiSession': 'eyJpZCI6Ijc1YzZhZDJjLWYxYTYtNDgxNC1iM2E4LTBiMjBmYzM5YzE0MyIsInJlZmVycmVyIjoibXlkcmFtYWxpc3QuY29tIiwiY2FtcGFpZ24iOnsic291cmNlIjpudWxsLCJtZWRpdW0iOm51bGwsImNhbXBhaWduIjpudWxsLCJ0ZXJtIjpudWxsLCJjb250ZW50IjpudWxsfX0=',
        'FCNEC': '%5B%5B%22AKsRol-50cg1WydoUmZE0JAjIAttaAf0y4-uHRiEWpABIOMRKnGfYYJ6W8XmpNA-3sAIoZO6q_7Q_aG7BuxzIdemPvw0pE3UD8iqQBxeOrVMxYaNb5EW0cLnvtvE--M2rAmMTk5PUfyUggnDl_GrcYTjVTPc9PCVrg%3D%3D%22%5D%5D',
        '_ga': 'GA1.2.88700865.1706404521',
        '_gid': 'GA1.2.544651336.1706550463',
        '_pbjs_userid_consent_data': '3524755945110770',
        '_au_1d': 'AU1D-0100-001706404523-CWZVC2BF-C6C6',
        '_au_last_seen_pixels': 'eyJhcG4iOjE3MDY1NTA0NTMsInR0ZCI6MTcwNjU1MDQ1MywicHViIjoxNzA2NTUwNDUzLCJydWIiOjE3MDY1NTA0NTMsInRhcGFkIjoxNzA2NTUwNDUzLCJhZHgiOjE3MDY1NTA0NTMsImdvbyI6MTcwNjU1MDQ1MywidW5ydWx5IjoxNzA2NTUwNDYxLCJpbmRleCI6MTcwNjU1MDQ2MSwic29uIjoxNzA2NTUwNDUzLCJiZWVzIjoxNzA2NTUwNDYxLCJvcGVueCI6MTcwNjU1MDQ1MywiY29sb3NzdXMiOjE3MDY1NTA0NjEsImFkbyI6MTcwNjQwNDUzMCwidGFib29sYSI6MTcwNjU1MDQ2MSwiYW1vIjoxNzA2NTUwNDYxLCJzbWFydCI6MTcwNjU1MDQ2MSwicHBudCI6MTcwNjU1MDQ2MSwiaW1wciI6MTcwNjU1MDQ2MX0%3D',
        '_ga_9MWM3T9VD7': 'GS1.1.1706550442.4.1.1706550457.45.0.0',
        'plsVisitorCity': 'Illinois',
        'plsVisitorGeo': 'US',
        '__gads': 'ID=4a6ff344140a1451:T=1706404523:RT=1706550453:S=ALNI_MYzG3rfX__dnSYdnI2waiSnLtmqng',
        '__gpi': 'UID=00000dba87ae3c77:T=1706404523:RT=1706550453:S=ALNI_MY5xQfLSYxo9rElGrkhtbcWB7M3WQ',
        'plsGeoObj': '{"ip":"73.36.161.220","country":"US","region":"IL","city":"Chicago","zip":"60615","location":"41.8018,-87.5993"}',
        'plsVisitorIp': '73.36.161.220',
        '_mdl_dm': '0',
        '__cflb': '04dToPqTexUPQvYwjCAo8qGUduzkzpTWEK5sawiL3M',
        '_lr_env_src_ats': 'false',
        'instUid': '5a06296f-33fa-4a7c-a58d-df69d8f50a96',
        '_mdl_vau': '5caabf9fa5ac9d3e10ffe52441604160',
        'jl_sess': 'b836098b4549056e4d1842a8e28c01cc0bc3e65c0338e8abe2434697e1f09951',
        '_cc_id': '5b5a20ce0acd4ab6a2ef45dbd5a13003',
        '_lc2_fpi': '41506042aaa6--01hn6t5ecjb1qhxgar1119f7hy',
        '_lc2_fpi_meta': '{%22w%22:1706404526483}',
        '_li_dcdm_c': '.mydramalist.com',
        '_pubcid': '0e6baf06-4808-400c-a697-7f89a09ead0c',
        'panoramaId': '148b98e223db4cd9561b5472e72c185ca02cdb3137449d7b90eceda6d776a5df',
        'panoramaId_expiry': '1707009326638',
        'pbjs-unifiedid': '%7B%22TDID%22%3A%2221cf0667-dcc0-4fed-8505-cba2a161276a%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-01-28T01%3A15%3A26%22%7D',
        '_ga': 'GA1.1.88700865.1706404521',
        'panoramaIdType': 'panoDevice',
        'instiPubProvided': 'ed30b669-5dd2-46d4-bd87-72583ebf3d8d',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'none',
        # 'Cookie': 'InstiSession=eyJpZCI6Ijc1YzZhZDJjLWYxYTYtNDgxNC1iM2E4LTBiMjBmYzM5YzE0MyIsInJlZmVycmVyIjoibXlkcmFtYWxpc3QuY29tIiwiY2FtcGFpZ24iOnsic291cmNlIjpudWxsLCJtZWRpdW0iOm51bGwsImNhbXBhaWduIjpudWxsLCJ0ZXJtIjpudWxsLCJjb250ZW50IjpudWxsfX0=; FCNEC=%5B%5B%22AKsRol-50cg1WydoUmZE0JAjIAttaAf0y4-uHRiEWpABIOMRKnGfYYJ6W8XmpNA-3sAIoZO6q_7Q_aG7BuxzIdemPvw0pE3UD8iqQBxeOrVMxYaNb5EW0cLnvtvE--M2rAmMTk5PUfyUggnDl_GrcYTjVTPc9PCVrg%3D%3D%22%5D%5D; _ga=GA1.2.88700865.1706404521; _gid=GA1.2.544651336.1706550463; _pbjs_userid_consent_data=3524755945110770; _au_1d=AU1D-0100-001706404523-CWZVC2BF-C6C6; _au_last_seen_pixels=eyJhcG4iOjE3MDY1NTA0NTMsInR0ZCI6MTcwNjU1MDQ1MywicHViIjoxNzA2NTUwNDUzLCJydWIiOjE3MDY1NTA0NTMsInRhcGFkIjoxNzA2NTUwNDUzLCJhZHgiOjE3MDY1NTA0NTMsImdvbyI6MTcwNjU1MDQ1MywidW5ydWx5IjoxNzA2NTUwNDYxLCJpbmRleCI6MTcwNjU1MDQ2MSwic29uIjoxNzA2NTUwNDUzLCJiZWVzIjoxNzA2NTUwNDYxLCJvcGVueCI6MTcwNjU1MDQ1MywiY29sb3NzdXMiOjE3MDY1NTA0NjEsImFkbyI6MTcwNjQwNDUzMCwidGFib29sYSI6MTcwNjU1MDQ2MSwiYW1vIjoxNzA2NTUwNDYxLCJzbWFydCI6MTcwNjU1MDQ2MSwicHBudCI6MTcwNjU1MDQ2MSwiaW1wciI6MTcwNjU1MDQ2MX0%3D; _ga_9MWM3T9VD7=GS1.1.1706550442.4.1.1706550457.45.0.0; plsVisitorCity=Illinois; plsVisitorGeo=US; __gads=ID=4a6ff344140a1451:T=1706404523:RT=1706550453:S=ALNI_MYzG3rfX__dnSYdnI2waiSnLtmqng; __gpi=UID=00000dba87ae3c77:T=1706404523:RT=1706550453:S=ALNI_MY5xQfLSYxo9rElGrkhtbcWB7M3WQ; plsGeoObj={"ip":"73.36.161.220","country":"US","region":"IL","city":"Chicago","zip":"60615","location":"41.8018,-87.5993"}; plsVisitorIp=73.36.161.220; _mdl_dm=0; __cflb=04dToPqTexUPQvYwjCAo8qGUduzkzpTWEK5sawiL3M; _lr_env_src_ats=false; instUid=5a06296f-33fa-4a7c-a58d-df69d8f50a96; _mdl_vau=5caabf9fa5ac9d3e10ffe52441604160; jl_sess=b836098b4549056e4d1842a8e28c01cc0bc3e65c0338e8abe2434697e1f09951; _cc_id=5b5a20ce0acd4ab6a2ef45dbd5a13003; _lc2_fpi=41506042aaa6--01hn6t5ecjb1qhxgar1119f7hy; _lc2_fpi_meta={%22w%22:1706404526483}; _li_dcdm_c=.mydramalist.com; _pubcid=0e6baf06-4808-400c-a697-7f89a09ead0c; panoramaId=148b98e223db4cd9561b5472e72c185ca02cdb3137449d7b90eceda6d776a5df; panoramaId_expiry=1707009326638; pbjs-unifiedid=%7B%22TDID%22%3A%2221cf0667-dcc0-4fed-8505-cba2a161276a%22%2C%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-01-28T01%3A15%3A26%22%7D; _ga=GA1.1.88700865.1706404521; panoramaIdType=panoDevice; instiPubProvided=ed30b669-5dd2-46d4-bd87-72583ebf3d8d',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'mydramalist.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Connection': 'keep-alive',
    }

    params = {
        'notes': '1',
    }

    response = requests.get('https://mydramalist.com/dramalist/Mystic_pub/completed', params=params, cookies=cookies, headers=headers)
    #response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    
    #driver = webdriver.Firefox()
    #driver.get('https://mydramalist.com/dramalist/Mystic_pub/completed?notes=1')
    #html = driver.page_source
    #soup = BeautifulSoup(html)
    return soup

def get_titles(soup):
    """
    Extracts list of k-drama titles.
    """
    cite_elements = soup.select('td[class^=mdl-style-col-title]')
    titles_list = [element.get_text(strip=True) for element in cite_elements]
    titles_edit1 = [s.replace('Korean Drama','') for s in titles_list]
    titles_edit2 = [s.replace('edit','') for s in titles_edit1]
    titles_edit3 = [s for s in titles_edit2 if 'Korean Movie' not in s]
    final_titles = [s for s in titles_edit3 if "Inferno" not in s]
    return final_titles

def get_reviews(soup):
    """
    Extracts list of k-drama reviews.
    """
    cite_elements_reviews = soup.select('td[class^=mdl-style-col-notes]')
    reviews = [element.get_text(strip=True) for element in cite_elements_reviews]
    final_reviews = [s for s in reviews if s != '']
    return final_reviews


# get soup, titles, and reviews
soup = get_data()
titles = get_titles(soup)
reviews = get_reviews(soup)


# join titles and reviews into a data frame and convert to csv
def save_df_to_csv(titles,reviews,filename,PATH):
    """
    Converts lists of titles and reviews to DataFrame and saves to a CSV file.
    This avoids having to get new cookies and headers for get_data() every time.
    """
    data = pd.DataFrame({'Title':titles,'Review':reviews})
    filepath = os.path.join(PATH,filename)
    data.to_csv(filepath,index=False,encoding='utf-8')

save_df_to_csv(titles, reviews, 'kdrama_data', '/Users/danya/Desktop/kdrama data')