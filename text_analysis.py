"""
Title: Text Analysis & Feature Extraction
@author: dsherbini
Date: February 2023
"""

# basic packages
import os
import pandas as pd
import matplotlib.pyplot as plt

# text analysis packages
import spacy
import nltk
from textblob import TextBlob
from nltk.corpus import wordnet
import re # regular expressions
from nltk.corpus import stopwords # stop words
#nltk.download('stopwords') # only need to run this once
from nltk.tokenize import word_tokenize # for word tokenization
from nltk.stem import WordNetLemmatizer # for stemming words
from sklearn.feature_extraction.text import CountVectorizer # for word counts
from wordcloud import WordCloud # for creating word cloud
from nltk import ngrams # for extracting phrases
from nltk.sentiment import SentimentIntensityAnalyzer # sentiment analysis

# set wd
PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

# import k-drama data
kdramas = pd.read_csv(os.path.join(PATH, 'kdrama_data'))

############################### TEXT PROCESSING ###############################

# first we need to clean the review text in order to analyze it further

# clean all text
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

# clean all reviews in the data frame
def clean_reviews(kdramas):
    '''
    Cleans the reviews in the kdrama dataframe using process_text() function.

    Parameters
    ----------
    kdramas: dataframe containing k-drama reviews

    Returns
    -------
    kdramas: updated dataframe with new column for clean reviews
    reviews_clean: list of clean reviews (list of list)
    '''
    reviews_to_clean = list(kdramas['Review'])
    reviews_clean = [process_text(r) for r in reviews_to_clean]
    kdramas['Reviews_Clean'] = reviews_clean
    return kdramas, reviews_clean

# get clean reviews
kdramas, reviews_clean = clean_reviews(kdramas)

################################# WORD COUNTS #################################

# start with basic text analysis: counting the freqency of individual words

# count common words
def get_common_words(reviews_clean):
    '''
    Counts the most common words using CountVectorizer.

    Parameters
    ----------
    reviews_clean: clean reviews as a list of lists

    Returns
    -------
    all_reviews: combined list of tokens from all reviews
    most_common_words: dictionary of all words and associated counts
    top_15_words: list of top 15 most common words and associated counts
    '''
    # initialize vectorizer
    vectorizer = CountVectorizer()

    # convert all reviews into one list of strings
    all_reviews = [word for review in reviews_clean for word in review]
    X = vectorizer.fit_transform(all_reviews)

    # get an array of all invidividual words from the reviews
    words = vectorizer.get_feature_names_out()

    # get word counts
    word_counts = X.toarray().sum(axis=0)

    # find the most common words
    most_common_words = dict(zip(words, word_counts))
    most_common_words_sorted = sorted(most_common_words.items(), key=lambda x: x[1], reverse=True)

    # top 15 most common words
    top_15_words = [(word, count) for word, count in most_common_words_sorted[:15]]

    return all_reviews, most_common_words, top_15_words

# get word counts
all_reviews, most_common_words, top_15_words = get_common_words(reviews_clean)

# create word cloud of common words
wordcloud = WordCloud(width=800, height=400, background_color='white', 
                      max_words=100).generate(' '.join(all_reviews))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

################################ PHRASE COUNTS ################################

# now we'll extract and count common phrases instead of words

# get list of noun phrases using TextBlob
def get_common_phrases(reviews):
    '''
    Generates list of phrases and counts the most common phrases using CountVectorizer.

    Parameters
    ----------
    reviews: list or column of reviews

    Returns
    -------
    noun_phrases_list_connected: list of all phrases (connected with an underscore)
    most_common_phrases: dictionary of all phrases and associated counts
    '''
    noun_phrases_list = []

    # generate phrases
    for review in reviews:
        pattern = re.compile(r'[^\w\s]')
        kind_of_clean_review = re.sub(pattern, '', review).strip()
        kind_of_clean_review = kind_of_clean_review.lower().strip()
        blob = TextBlob(kind_of_clean_review)
        noun_phrases = list(blob.noun_phrases)
        noun_phrases_list.append(noun_phrases)

    # count the most common phrases
    # in order to use CountVectorizer we need to make each phrase into one term
    noun_phrases_list_connected = [phrase.replace(' ', '_') for phrases in noun_phrases_list for phrase in phrases]

    # initialize vectorizer to count common phrases
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(noun_phrases_list_connected)

    # get an array of all phrases
    phrases = vectorizer.get_feature_names_out()

    # get phrase counts
    phrase_counts = X.toarray().sum(axis=0)

    # find the most common phrases
    most_common_phrases = dict(zip(phrases, phrase_counts))
    
    return noun_phrases_list_connected, most_common_phrases


noun_phrases_list_connected, most_common_phrases = get_common_phrases(kdramas['Review'])

# create word cloud of common phrases
wordcloud2 = WordCloud(width=800, height=400, background_color='white', 
                      max_words=100).generate(' '.join(noun_phrases_list_connected))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis('off')
plt.show()
