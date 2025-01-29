"""
Title: Web Scraping Data from My Drama List - v2
@author: dsherbini
Date Created: January 2025
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import configparser
import ast

def load_config():
    """
    Loads the config.ini file and returns cookies, headers, and params as dictionaries.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Convert strings to dictionaries using ast.literal_eval
    try:
        cookies = ast.literal_eval(config['cookies']['cookies'])
    except KeyError:
        print("Error: 'cookies' section or 'cookies' key is missing in config.ini")
        cookies = {}
    
    try:
        headers = ast.literal_eval(config['headers']['headers'])
    except KeyError:
        print("Error: 'headers' section or 'headers' key is missing in config.ini")
        headers = {}
    
    try:
        params = ast.literal_eval(config['params']['params'])
    except KeyError:
        print("Error: 'params' section or 'params' key is missing in config.ini")
        params = {}
    
    return params, cookies, headers


cookies = {
    '_ga_9MWM3T9VD7': 'GS1.1.1738169266.1.1.1738169431.37.0.0',
    'hb_insticator_uid': 'c96f623d-b893-4604-96b2-f7deea933937',
    'cto_bidid': 'x85JnV9wdlNHSnRuYkFwNWp6QVQlMkI5QjJsUnhEcGNVWiUyRnI1Nm55VGFBbGdrT0xyc3lGa25UVnhodWZGaXRybFY2UnVXckppMnI4czJHT1k2OEo4RmRvUjlWQWclM0QlM0Q',
    'cto_bundle': 'Ucljhl94MVFJcXg0RGxWNVdIN2J1elYyN1I5YldxTXElMkY4VlVNZlFUR1d1SktHbWI1UE52MDlFbHg4eWExRWp2aXFyVWQxQ2ZEY2pySGczcTM1Q3o2VUJ5SVZmOVZiVTZFRmhFeGx1dzd5VnpKREZVUlFlJTJGbEtCQiUyRjZ3a1lJUU90S3diJTJG',
    '_au_1d': 'AU1D-0100-001738169268-HV02G0E6-PI3X',
    '_au_1d': 'AU1D-0100-001738169268-HV02G0E6-PI3X',
    '_ga': 'GA1.1.1253615785.1738169267',
    'plsVisitorCity': 'Illinois',
    'plsVisitorGeo': 'US',
    '_ga_FVWZ0RM4DH': 'GS1.1.1738169277.1.1.1738169408.60.0.0',
    '_mdl_dm': '0',
    '_ga': 'GA1.1.1253615785.1738169267',
    '_gid': 'GA1.1.1352141570.1738169289',
    '_mdl_vau': '5caabf9fa5ac9d3e10ffe52441604160',
    'jl_sess': '8884dea75f709818d1bd6d75fb6541554ef3306f8968e2cf9717c946be597a5e',
    '_sharedID': '3110057a-dfcd-4df9-a5e4-cbcb89b86f51',
    '_sharedID_cst': 'zix7LPQsHA%3D%3D',
    '__eoi': 'ID=48c0ecb23bdf446d:T=1738169268:RT=1738169268:S=AA-AfjZoOL0nGzC1GdxogAjz974f',
    '__gads': 'ID=b012a50c85f561e3:T=1738169268:RT=1738169268:S=ALNI_MYqyJLRVdy-gZn3C_4vQQUj4Spvmw',
    '__gpi': 'UID=00000fdbdefd72fa:T=1738169268:RT=1738169268:S=ALNI_MbQydaFj7SGMBnI23iCaaeJfZ5W3g',
    '_lc2_fpi': '41506042aaa6--01jjsfce1p06wtn5pjz9nyggpa',
    '_lc2_fpi_js': '41506042aaa6--01jjsfce1p06wtn5pjz9nyggpa',
    '33acrossIdFp': '0eL0yrWi0Ps7nKV%2BaWKgBMRJy8oSL89W3Bj25WtiOY5NUIPk3SxQJdJjSmsWWqq2nm8Maw2PXFoZsYME%2FKjs0g%3D%3D',
    '_cc_id': '91dd1ea578d99bd042594e3201ab972c',
    '_pubcid': '934068b7-b9b4-4c47-ae1b-56ffbc9390c7',
    '_pubcid_cst': 'zix7LPQsHA%3D%3D',
    'panoramaId': 'a289a7f631e89f71fb88127fb27f16d53938ade29873320aa27c75f875b3af04',
    'panoramaId_expiry': '1738774067310',
    '_lr_env_src_ats': 'false',
    'instiPubProvided': 'e91f6d92-c935-4bc7-9157-0a8c5d8b369a',
    'plsGeoObj': '{"ip":"2601:240:c402:6310:bd58:da92:730e:4aea","country":"US","region":"IL","city":"Chicago","zip":"60615","location":"41.8018,-87.5993"}',
    'plsVisitorIp': '2601:240:c402:6310:bd58:da92:730e:4aea',
    'bid-46767-46766_5-95': '46766',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'same-origin',
    # 'Cookie': '_ga_9MWM3T9VD7=GS1.1.1738169266.1.1.1738169431.37.0.0; hb_insticator_uid=c96f623d-b893-4604-96b2-f7deea933937; cto_bidid=x85JnV9wdlNHSnRuYkFwNWp6QVQlMkI5QjJsUnhEcGNVWiUyRnI1Nm55VGFBbGdrT0xyc3lGa25UVnhodWZGaXRybFY2UnVXckppMnI4czJHT1k2OEo4RmRvUjlWQWclM0QlM0Q; cto_bundle=Ucljhl94MVFJcXg0RGxWNVdIN2J1elYyN1I5YldxTXElMkY4VlVNZlFUR1d1SktHbWI1UE52MDlFbHg4eWExRWp2aXFyVWQxQ2ZEY2pySGczcTM1Q3o2VUJ5SVZmOVZiVTZFRmhFeGx1dzd5VnpKREZVUlFlJTJGbEtCQiUyRjZ3a1lJUU90S3diJTJG; _au_1d=AU1D-0100-001738169268-HV02G0E6-PI3X; _au_1d=AU1D-0100-001738169268-HV02G0E6-PI3X; _ga=GA1.1.1253615785.1738169267; plsVisitorCity=Illinois; plsVisitorGeo=US; _ga_FVWZ0RM4DH=GS1.1.1738169277.1.1.1738169408.60.0.0; _mdl_dm=0; _ga=GA1.1.1253615785.1738169267; _gid=GA1.1.1352141570.1738169289; _mdl_vau=5caabf9fa5ac9d3e10ffe52441604160; jl_sess=8884dea75f709818d1bd6d75fb6541554ef3306f8968e2cf9717c946be597a5e; _sharedID=3110057a-dfcd-4df9-a5e4-cbcb89b86f51; _sharedID_cst=zix7LPQsHA%3D%3D; __eoi=ID=48c0ecb23bdf446d:T=1738169268:RT=1738169268:S=AA-AfjZoOL0nGzC1GdxogAjz974f; __gads=ID=b012a50c85f561e3:T=1738169268:RT=1738169268:S=ALNI_MYqyJLRVdy-gZn3C_4vQQUj4Spvmw; __gpi=UID=00000fdbdefd72fa:T=1738169268:RT=1738169268:S=ALNI_MbQydaFj7SGMBnI23iCaaeJfZ5W3g; _lc2_fpi=41506042aaa6--01jjsfce1p06wtn5pjz9nyggpa; _lc2_fpi_js=41506042aaa6--01jjsfce1p06wtn5pjz9nyggpa; 33acrossIdFp=0eL0yrWi0Ps7nKV%2BaWKgBMRJy8oSL89W3Bj25WtiOY5NUIPk3SxQJdJjSmsWWqq2nm8Maw2PXFoZsYME%2FKjs0g%3D%3D; _cc_id=91dd1ea578d99bd042594e3201ab972c; _pubcid=934068b7-b9b4-4c47-ae1b-56ffbc9390c7; _pubcid_cst=zix7LPQsHA%3D%3D; panoramaId=a289a7f631e89f71fb88127fb27f16d53938ade29873320aa27c75f875b3af04; panoramaId_expiry=1738774067310; _lr_env_src_ats=false; instiPubProvided=e91f6d92-c935-4bc7-9157-0a8c5d8b369a; plsGeoObj={"ip":"2601:240:c402:6310:bd58:da92:730e:4aea","country":"US","region":"IL","city":"Chicago","zip":"60615","location":"41.8018,-87.5993"}; plsVisitorIp=2601:240:c402:6310:bd58:da92:730e:4aea; bid-46767-46766_5-95=46766',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.15',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://mydramalist.com/dramalist/Mystic_pub',
    'Priority': 'u=0, i',
}

params = {
    'notes': '1',
}



def get_data():
    """
    Retrieves data from My Drama List website. Because the website requires an account login, 
    this function uses cookies and headers converted to python from cURL in order to create the soup.
    Source: https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup
    """
    # load config
   # params, cookies, headers = load_config()
    
    # determine url
    url = 'https://mydramalist.com/dramalist/Mystic_pub/completed'
    
    # get response
    response = requests.get(url=url, params=params, cookies=cookies, headers=headers)
    
    # get soup
    soup = BeautifulSoup(response.text,'html.parser')
    
    return soup


soup = get_data()
print(soup.prettify())


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


# join titles and reviews into a data frame
def get_dramas(titles, reviews):
    """
    Convert soup, titles, and reviews to final dataframe.
    """
    # combine titles and reviews into dataframe
    data = pd.DataFrame({'Title':titles,'Review':reviews})
    
    # remove a few movies from the dataframe
    movie1 = data[data['Title'] == '20th Century Girl'].index
    movie2 = data[data['Title'] == 'Love and Leashes'].index
    movie3 = data[data['Title'] == 'Tune in for Love'].index
    data = data.drop(movie1)
    data = data.drop(movie2)
    data = data.drop(movie3)
    
    return data

my_dramas = get_dramas(titles, reviews)