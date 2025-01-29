"""
Title: Web Scraping Data from My Drama List
@author: dsherbini
Date Created: January 2024
Last Updated: Oct 2024
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
        'FCNEC': '%5B%5B%22AKsRol8LeV6YgD-FBubzW5wyKOlGBNFy41hNs5vVQrg_vGImISHzLuS5yHNmERLtsBR7VspKDt5uhudJqC4erXJb2sgTLLxCWWD54yyaXTBfk1qz6fzctYR6pWJaJfr5scu_lma0MbPqQFxjZDVc2KgvqV3ChiNBTQ%3D%3D%22%5D%5D',
        '__eoi': 'ID=b2b7977e9a11cd30:T=1728086256:RT=1728090300:S=AA-AfjaTWuPmGyZBFgfNTNxSccmn',
        '__gads': 'ID=87b0a1266201a393:T=1728086256:RT=1728090300:S=ALNI_MblGiwKA5OaYHgYkYZCsb9xg029aA',
        '__gpi': 'UID=00000f3539b9af37:T=1728086256:RT=1728090300:S=ALNI_MZYc7fdacQEuHHCnXWNJsUBDk58JA',
        '_au_1d': 'AU1D-0100-001728086256-424I0ELF-19JE',
        '_ga': 'GA1.2.1323443072.1728086255',
        '_ga_9MWM3T9VD7': 'GS1.1.1728089609.2.1.1728090298.59.0.0',
        '_gid': 'GA1.2.492839727.1728086258',
        'InstiSession': 'eyJpZCI6IjFmZjdiNjc0LTk4ODQtNDgzNi1iZjBkLWRjYjhlZmQyMjAwYSIsInJlZmVycmVyIjoibXlkcmFtYWxpc3QuY29tIiwiY2FtcGFpZ24iOnsic291cmNlIjpudWxsLCJtZWRpdW0iOm51bGwsImNhbXBhaWduIjpudWxsLCJ0ZXJtIjpudWxsLCJjb250ZW50IjpudWxsfX0=',
        'plsVisitorCity': 'Illinois',
        'plsVisitorGeo': 'US',
        '_ga_FVWZ0RM4DH': 'GS1.1.1728089678.2.1.1728090297.60.0.0',
        '_mdl_dm': '0',
        '_mdl_logged': '1728090367',
        '__cflb': '04dToPqTexUPQvYwjCAo8qGUduzkzpTWNndDjEQzsV',
        'cto_bundle': 'ApktxV96V0lyUUl0TkV4dXJaZjJ5VlZZUWpBTnRuSmptVXNZNnVPaDNQZ0tyZXFFUGRrNWhHeUcxM0VEa20yTWxtSjNUNWpuMTQ2RjNZdFNiVDdna3ZON3pLQTlsOWQydWhneTdDSURQYnYwT2dzdWxoWFlvVDNleHkwVlBxSXNsenhpTw',
        'hb_insticator_uid': 'b13561a9-e536-47dc-b345-0b56c1e1d111',
        '_mdl_vau': '5caabf9fa5ac9d3e10ffe52441604160',
        'jl_sess': 'f20a5aa75b79a6cd48ba914857dd0c37005dc55ed8a63e5168f576c9c540a1be',
        'cto_bidid': 'hIr8Q19SbzBDVVV5NkdmODR3SWdjOSUyQmZPT3B6ZTVZNDElMkZOWHRQSzJCNWFjZkxWWU0lMkIlMkZ1aG8lMkJJVFAyTE9LQ3kyZVI1eCUyQnU3ZDE4d1F5Nk5wdUJDbGc5TExtZyUzRCUzRA',
        '_cc_id': 'aa203554cbae3dd2ea8c8c11764c3abf',
        'panoramaId_expiry': '1728172660104',
        '_lc2_fpi': '41506042aaa6--01j9czfe3xgf681jcz7v6bp2a1',
        '_li_dcdm_c': '.mydramalist.com',
        '_pubcid': 'f67af9f9-a06d-4972-980a-c9e109d08378',
        '_pubcid_cst': 'zix7LPQsHA%3D%3D',
        '_lr_env_src_ats': 'false',
        '33acrossIdFp': '%2B3wZerla%2BsxZtnyyUEqwar%2BEMLaQwxcStP785WfJ9Z%2F4aIYOXTc8F0u3Y64pa8G4hyv0NxKWHza95VezQIdu%2FA%3D%3D',
        '__qca': 'I0-588004007-1728086256151',
        'instiPubProvided': '4b57290c-7893-4568-bb98-4958e92409f8',
        'plsGeoObj': '{"ip":"140.248.30.69","country":"US","region":"IL","city":"Schaumburg","zip":"60159","location":"42.0317,-88.0833"}',
        'plsVisitorIp': '140.248.30.69',
    }
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        # 'Cookie': 'FCNEC=%5B%5B%22AKsRol8LeV6YgD-FBubzW5wyKOlGBNFy41hNs5vVQrg_vGImISHzLuS5yHNmERLtsBR7VspKDt5uhudJqC4erXJb2sgTLLxCWWD54yyaXTBfk1qz6fzctYR6pWJaJfr5scu_lma0MbPqQFxjZDVc2KgvqV3ChiNBTQ%3D%3D%22%5D%5D; __eoi=ID=b2b7977e9a11cd30:T=1728086256:RT=1728090300:S=AA-AfjaTWuPmGyZBFgfNTNxSccmn; __gads=ID=87b0a1266201a393:T=1728086256:RT=1728090300:S=ALNI_MblGiwKA5OaYHgYkYZCsb9xg029aA; __gpi=UID=00000f3539b9af37:T=1728086256:RT=1728090300:S=ALNI_MZYc7fdacQEuHHCnXWNJsUBDk58JA; _au_1d=AU1D-0100-001728086256-424I0ELF-19JE; _ga=GA1.2.1323443072.1728086255; _ga_9MWM3T9VD7=GS1.1.1728089609.2.1.1728090298.59.0.0; _gid=GA1.2.492839727.1728086258; InstiSession=eyJpZCI6IjFmZjdiNjc0LTk4ODQtNDgzNi1iZjBkLWRjYjhlZmQyMjAwYSIsInJlZmVycmVyIjoibXlkcmFtYWxpc3QuY29tIiwiY2FtcGFpZ24iOnsic291cmNlIjpudWxsLCJtZWRpdW0iOm51bGwsImNhbXBhaWduIjpudWxsLCJ0ZXJtIjpudWxsLCJjb250ZW50IjpudWxsfX0=; plsVisitorCity=Illinois; plsVisitorGeo=US; _ga_FVWZ0RM4DH=GS1.1.1728089678.2.1.1728090297.60.0.0; _mdl_dm=0; _mdl_logged=1728090367; __cflb=04dToPqTexUPQvYwjCAo8qGUduzkzpTWNndDjEQzsV; cto_bundle=ApktxV96V0lyUUl0TkV4dXJaZjJ5VlZZUWpBTnRuSmptVXNZNnVPaDNQZ0tyZXFFUGRrNWhHeUcxM0VEa20yTWxtSjNUNWpuMTQ2RjNZdFNiVDdna3ZON3pLQTlsOWQydWhneTdDSURQYnYwT2dzdWxoWFlvVDNleHkwVlBxSXNsenhpTw; hb_insticator_uid=b13561a9-e536-47dc-b345-0b56c1e1d111; _mdl_vau=5caabf9fa5ac9d3e10ffe52441604160; jl_sess=f20a5aa75b79a6cd48ba914857dd0c37005dc55ed8a63e5168f576c9c540a1be; cto_bidid=hIr8Q19SbzBDVVV5NkdmODR3SWdjOSUyQmZPT3B6ZTVZNDElMkZOWHRQSzJCNWFjZkxWWU0lMkIlMkZ1aG8lMkJJVFAyTE9LQ3kyZVI1eCUyQnU3ZDE4d1F5Nk5wdUJDbGc5TExtZyUzRCUzRA; _cc_id=aa203554cbae3dd2ea8c8c11764c3abf; panoramaId_expiry=1728172660104; _lc2_fpi=41506042aaa6--01j9czfe3xgf681jcz7v6bp2a1; _li_dcdm_c=.mydramalist.com; _pubcid=f67af9f9-a06d-4972-980a-c9e109d08378; _pubcid_cst=zix7LPQsHA%3D%3D; _lr_env_src_ats=false; 33acrossIdFp=%2B3wZerla%2BsxZtnyyUEqwar%2BEMLaQwxcStP785WfJ9Z%2F4aIYOXTc8F0u3Y64pa8G4hyv0NxKWHza95VezQIdu%2FA%3D%3D; __qca=I0-588004007-1728086256151; instiPubProvided=4b57290c-7893-4568-bb98-4958e92409f8; plsGeoObj={"ip":"140.248.30.69","country":"US","region":"IL","city":"Schaumburg","zip":"60159","location":"42.0317,-88.0833"}; plsVisitorIp=140.248.30.69',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Mode': 'navigate',
        'Host': 'mydramalist.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
        'Referer': 'https://mydramalist.com/dramalist/Mystic_pub/completed',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    params = {
        'notes': '1',
    }
    
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


# get soup, titles, and reviews
soup = get_data()
titles = get_titles(soup)
reviews = get_reviews(soup)

# join titles and reviews into a data frame
def get_dramas():
    """
    Converts lists of titles and reviews to DataFrame.
    """
    data = pd.DataFrame({'Title':titles,'Review':reviews})
    # removing a few movies from the dataframe
    movie1 = data[data['Title'] == '20th Century Girl'].index
    movie2 = data[data['Title'] == 'Love and Leashes'].index
    movie3 = data[data['Title'] == 'Tune in for Love'].index
    data = data.drop(movie1)
    data = data.drop(movie2)
    data = data.drop(movie3)
    return data