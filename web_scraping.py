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
    # cookies from site
    cookies = {
        '_ga_9MWM3T9VD7': 'GS1.1.1710268212.1.1.1710268822.48.0.0',
        'FCNEC': '%5B%5B%22AKsRol-yvNPp3-jFu3xROeD7vfvhdr93H7iWOLYncI3kltzVa6MajB_zU7WHUKQ_BBkYo-S1KY7pINAFPskGW0t9SgW3ahtSEeDTz1-S3x4ftgK7NXm2FSWx4orY5iMhcq4WIl6jAX1yafJKHTeti_FykUSSFE9RZw%3D%3D%22%5D%5D',
        'InstiSession': 'eyJpZCI6ImEwMmM5YmIxLTM1MDktNDUxYi1iYzMxLTZkNDMxNmRiYWQyOCIsInJlZmVycmVyIjoiIiwiY2FtcGFpZ24iOnsic291cmNlIjpudWxsLCJtZWRpdW0iOm51bGwsImNhbXBhaWduIjpudWxsLCJ0ZXJtIjpudWxsLCJjb250ZW50IjpudWxsfX0=',
        '_au_1d': 'AU1D-0100-001710268213-7ACN1RPK-AIFK',
        '_ga': 'GA1.2.64662309.1710268212',
        '_gid': 'GA1.2.1541753162.1710268214',
        '_pbjs_userid_consent_data': '3524755945110770',
        'plsVisitorCity': 'Illinois',
        'plsVisitorGeo': 'US',
        '_ga_FVWZ0RM4DH': 'GS1.1.1710268221.1.1.1710268819.35.0.0',
        '_mdl_dm': '0',
        '_mdl_logged': '1710268765',
        '__eoi': 'ID=b24da2f1a68eced4:T=1710268213:RT=1710268751:S=AA-AfjZCj3aQT66nQfz0Quu3WtOr',
        '__gads': 'ID=7689928fb6cfb7df:T=1710268213:RT=1710268751:S=ALNI_MZjYEC8GasxrNBQ_GWqDhtwjmeMyg',
        '__gpi': 'UID=00000dd1df98af49:T=1710268213:RT=1710268751:S=ALNI_Mbkl9kR7wUh4-5a5GH14uDFYbkYqw',
        '__qca': 'I0-1557893108-1710268223350',
        'instUid': '4f3c8f2c-8ffd-420c-b201-2b2a9cb6f9bd',
        '_mdl_vau': '5caabf9fa5ac9d3e10ffe52441604160',
        'jl_sess': '8f8bab3ba0cd0788b169ccdac6e1fa7ca0a53edb1cc3f465d31d8d0ce36004d0',
        '_cc_id': 'be2460d307a6f0220f0ba5d419ebd0aa',
        '_pubcid': 'ba8abc78-2731-42d3-a919-64cd8620cc59',
        'panoramaId': '148b98e223db4cd9561b5472e72c185ca02cdb3137449d7b90eceda6d776a5df',
        'panoramaIdType': 'panoDevice',
        'panoramaId_expiry': '1710873012804',
        'instiPubProvided': '427114fc-ee9c-478c-bd75-06efd2a0d3d4',
        'plsGeoObj': '{"ip":"73.36.161.220","country":"US","region":"IL","city":"Chicago","zip":"60637","location":"41.7821,-87.6046"}',
        'plsVisitorIp': '73.36.161.220',
        '__cflb': '04dToPqTexUPQvYwjCAo8qGUduzkzpTVDzCume6Kx7',
    }
    
    # headers from the site. leave comments as is.
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        # 'Cookie': '_ga_9MWM3T9VD7=GS1.1.1710268212.1.1.1710268822.48.0.0; FCNEC=%5B%5B%22AKsRol-yvNPp3-jFu3xROeD7vfvhdr93H7iWOLYncI3kltzVa6MajB_zU7WHUKQ_BBkYo-S1KY7pINAFPskGW0t9SgW3ahtSEeDTz1-S3x4ftgK7NXm2FSWx4orY5iMhcq4WIl6jAX1yafJKHTeti_FykUSSFE9RZw%3D%3D%22%5D%5D; InstiSession=eyJpZCI6ImEwMmM5YmIxLTM1MDktNDUxYi1iYzMxLTZkNDMxNmRiYWQyOCIsInJlZmVycmVyIjoiIiwiY2FtcGFpZ24iOnsic291cmNlIjpudWxsLCJtZWRpdW0iOm51bGwsImNhbXBhaWduIjpudWxsLCJ0ZXJtIjpudWxsLCJjb250ZW50IjpudWxsfX0=; _au_1d=AU1D-0100-001710268213-7ACN1RPK-AIFK; _ga=GA1.2.64662309.1710268212; _gid=GA1.2.1541753162.1710268214; _pbjs_userid_consent_data=3524755945110770; plsVisitorCity=Illinois; plsVisitorGeo=US; _ga_FVWZ0RM4DH=GS1.1.1710268221.1.1.1710268819.35.0.0; _mdl_dm=0; _mdl_logged=1710268765; __eoi=ID=b24da2f1a68eced4:T=1710268213:RT=1710268751:S=AA-AfjZCj3aQT66nQfz0Quu3WtOr; __gads=ID=7689928fb6cfb7df:T=1710268213:RT=1710268751:S=ALNI_MZjYEC8GasxrNBQ_GWqDhtwjmeMyg; __gpi=UID=00000dd1df98af49:T=1710268213:RT=1710268751:S=ALNI_Mbkl9kR7wUh4-5a5GH14uDFYbkYqw; __qca=I0-1557893108-1710268223350; instUid=4f3c8f2c-8ffd-420c-b201-2b2a9cb6f9bd; _mdl_vau=5caabf9fa5ac9d3e10ffe52441604160; jl_sess=8f8bab3ba0cd0788b169ccdac6e1fa7ca0a53edb1cc3f465d31d8d0ce36004d0; _cc_id=be2460d307a6f0220f0ba5d419ebd0aa; _pubcid=ba8abc78-2731-42d3-a919-64cd8620cc59; panoramaId=148b98e223db4cd9561b5472e72c185ca02cdb3137449d7b90eceda6d776a5df; panoramaIdType=panoDevice; panoramaId_expiry=1710873012804; instiPubProvided=427114fc-ee9c-478c-bd75-06efd2a0d3d4; plsGeoObj={"ip":"73.36.161.220","country":"US","region":"IL","city":"Chicago","zip":"60637","location":"41.7821,-87.6046"}; plsVisitorIp=73.36.161.220; __cflb=04dToPqTexUPQvYwjCAo8qGUduzkzpTVDzCume6Kx7',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'mydramalist.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15',
        'Referer': 'https://mydramalist.com/dramalist/Mystic_pub',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    # params
    params = {
        'notes': '1',
        }
    
    # get response from cookies, headers, and params above using below URL
    response = requests.get('https://mydramalist.com/dramalist/Mystic_pub/completed', params=params, cookies=cookies, headers=headers)
    
    # get soup
    soup = BeautifulSoup(response.content,'html.parser')
    
    return soup

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
    titles_edit2 = [s.replace('edit','') for s in titles_edit1]
    
    # filter out any movies or tv shows (want kdramas only)
    titles_edit3 = [s for s in titles_edit2 if 'Korean Movie' not in s]
    final_titles = [s for s in titles_edit3 if 'Inferno' not in s]
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