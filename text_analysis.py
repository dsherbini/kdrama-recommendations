"""
Title: Text Analysis & Feature Extraction
@author: dsherbini
Date: February 2023
"""

import os
import pandas as pd
import nltk
import re
from textblob import TextBlob
from nltk.corpus import wordnet
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy

PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

# import k-drama data
kdramas = pd.read_csv(os.path.join(PATH, 'kdrama_data'))

############################### TEXT PROCESSING ###############################

def process_text(raw_text):
    '''
    Cleans text and prepares for analysis by:
        - removing punctuation
        - making lowercase
        - tokenizing text
        - removing stop words
        - stemming: breaking down words to their root
    
    Parameters
    ----------
    raw_text: string of original raw text

    Returns
    -------
    final_text: string of new processed text
    '''
    
    # remove punctiation
    pattern = re.compile(r'[^\w\s]')
    clean_text1 = re.sub(pattern, '', raw_text).strip()
    
    # make lowercase
    clean_text2 = clean_text1.lower().strip()
    
    # tokenize
    clean_text3 = word_tokenize(clean_text2) 
    
    # remove stop words
    stop_words = set(stopwords.words('english'))
    clean_text4 = [w for w in clean_text3 if w not in stop_words]
    
    # stem/lemmatize words
    lemmatizer = WordNetLemmatizer()
    final_text = [lemmatizer.lemmatize(w) for w in clean_text4]
    
    return final_text

process_text(kdramas['Review'].iloc[0])
