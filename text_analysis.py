"""
Title: Text Analysis & Feature Extraction
@author: dsherbini
Date: February 2023
"""

# basic packages
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# text analysis packages
import spacy
import nltk
# nltk.download('punkt') # only need to run this once
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

# get phrase counts
noun_phrases_list_connected, most_common_phrases = get_common_phrases(kdramas['Review'])

# create word cloud of common phrases
wordcloud2 = WordCloud(width=800, height=400, background_color='white', 
                      max_words=100).generate(' '.join(noun_phrases_list_connected))

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis('off')
plt.show()


############################# SIMILARITY ANALYSIS #############################

# now we will take the list of phrases and measure their similarity (i.e. phrase embedding) using Gensim packages
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity

# load Google's pre-trained Word2Vec model
model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

# remove underscore from phrases/split into individual words
phrases = noun_phrases_list_connected
words = [phrase.split('_') for phrase in phrases]

# write function to calculate phrase similarity
def calculate_phrase_similarity(phrase1, phrase2, model):
    ''' Calculate the similarity between two phrases using the cosine similarity between average embeddings.

    Parameters
    ----------
    phrase1: phrase to use for comparison (string)
    phrase2: phrase to use for comparison (string)
    model: your trained word2vec model of choice

    Returns
    -------
    similarity: a score between 0 to 1. A score of 1 means the two phrases are identical.
    A score of 0 means the two words are not present in the training data.
    '''
    # split the phrases into individual words for easier processing
    words1 = phrase1.split('_')
    words2 = phrase2.split('_')
    
    # filter out words not in the model's vocabulary
    words1 = [word for word in words1 if word in model.wv]
    words2 = [word for word in words2 if word in model.wv]
    
    # if both phrases are empty after filtering, return a similarity score of 0
    if not words1 or not words2:
        return 0.0
    
    # calculate the average embedding for each phrase
    avg_embedding1 = sum(model.wv[word] for word in words1) / len(words1)
    avg_embedding2 = sum(model.wv[word] for word in words2) / len(words2)
    
    # calculate the cosine similarity between the average embeddings
    similarity = cosine_similarity([avg_embedding1], [avg_embedding2])[0][0]
    
    # return numerical score
    return similarity


# find very similar phrases
def get_similar_phrases(phrases, similarity_min, similarity_max):
    '''
    Get similar phrases by setting min and max similarity score thresholds.

    Parameters
    ----------
    phrases: list of phrases to analyze (list of strings)
    similarity_min: minimum similarity score (must be between 0 and 1)
    similarity_max: maximum similarity score (must be between 0 and 1)

    Returns
    -------
    similar_phrases: a dataframe of compared phrases and their similarity scores
    '''
    phrase_1 = []
    phrase_2 = []
    scores = []
    for i in range(len(phrases)):
        for j in range(i+1, len(phrases)):
            similarity = calculate_phrase_similarity(phrases[i], phrases[j], model)
            if similarity >= similarity_min and similarity < similarity_max:
                phrase_1.append(phrases[i])
                phrase_2.append(phrases[j])
                scores.append(similarity)
    similar_phrases = pd.DataFrame({'Phrase1':phrase_1, 'Phrase2':phrase_2, 'Similarity_Score':scores})
    return similar_phrases

# get similar phrases
# note: this takes 45 seconds - 1 minute to run
similar_phrases = get_similar_phrases(phrases, .8, .95)


############################# SENTIMENT ANALYSIS ##############################

# now we'll conduct sentiment analyses -- both general and for certain phrases

# general sentiment analysis of each review
def sentiment_reviews(df, reviews):
    '''
    Get polarity scores for each k-drama review.

    Parameters
    ----------
    reviews: list or column containing original review text

    Returns
    -------
    adds a column in the dataframe for polarity score
        - polarity score refers to how positive or negative a set of text is
        - scores closer to 1 are more positive
        - scores closer to -1 are more negative
        - scores closer to 0 are more neutral
    '''
    polarity_scores = []
    # create a TextBlob object
    for r in reviews:
        blob = TextBlob(r)

        # perform sentiment analysis
        sentiment = blob.sentiment
        polarity_scores.append(sentiment.polarity)
    df['Polarity_Score'] = polarity_scores
    return df

kdramas = sentiment_reviews(kdramas, kdramas['Review'])

# sentiment analysis for specific phrases
def sentiment_around_phrase(sentence, phrase):
    '''
    Get polarity score of text surrounding a specific phrase.

    Parameters
    ----------
    sentence: text to analyze
    phrase: specific phrase within the text to analyze

    Returns
    -------
    phrase_sentiment: average polarity score of text before and after the target phrase (-1 to 1)
    '''
    # convert to lowercase
    sentence_lower = sentence.lower()
    phrase_lower = phrase.lower()
    
    # find the start and end indices of the phrase in the sentence
    if phrase_lower in sentence_lower:
        start_index = sentence_lower.find(phrase_lower)
        end_index = start_index + len(phrase_lower)
    
        # extract the text before and after the phrase
        before_phrase = sentence[:start_index]
        after_phrase = sentence[end_index:]
    
        # get polarity score of text before and after the phrase
        before_sentiment = TextBlob(before_phrase).sentiment.polarity
        after_sentiment = TextBlob(after_phrase).sentiment.polarity
    
        # get average sentiment of the surrounding context
        phrase_sentiment = (before_sentiment + after_sentiment) / 2
        return phrase_sentiment

# get sentiment for a list of phrases, for all reviews
target_phrases = ['female lead', 'FL', 'second female lead', 'male lead', 'ML', 'second male lead',
                  'cast', 'main leads', 'ensemble cast', 'couple', 'side couples', 'plot', 'story', 
                  'beginning', 'ending', 'romance', 'acting']

# add sentiment scores as features in the data frame
for phrase in target_phrases:
    kdramas[f'sentiment_{phrase}'] = kdramas['Review'].apply(lambda x: sentiment_around_phrase(x, phrase))


############################# FEATURE EXTRACTION ##############################

# now we will create some features in out data set based on most common words 
# and phrases found in the previous analyses

def get_feature(df, text_column, new_column, word_list):
    '''
    Creates a binary feature in the k-drama data set if a list of relevant words 
    exist in the review.
    
    Parameters
    ----------
    df: data frame of interest
    text_column: column in df containing text to scan (string)
    new_column: name of new column (string)
    word_list: list of relevant words to search for in the review column

    Returns
    -------
    DataFrame with the new column added
    '''
    # check to see if text column contains any word from specified list
    def contains_word(text_column):
        return 1 if any(word in text_column for word in word_list) else 0
    
    # apply contains_word function to create new column for the feature
    df[new_column] = df[text_column].apply(contains_word)
    
    return df

# create features based on the following target words
feature_dict = {
    'romance': ['romance', 'chemistry', 'cute', 'swoon'],
    'kiss': ['kiss'],
    'comedy':['comedy', 'comedic', 'funny', 'hilarious', 'laugh', 'laughed'],
    'melodrama': ['melodrama', 'melodramatic'],
    'wholesome': ['wholesome', 'sweet'],
    'sad': ['sad', 'tear', 'tears', 'cry', 'bawl', 'bawling', 'tragic', 'heavy', 'suicide'],
    'slow burn': ['slow', 'burn', 'boring'],
    'tropey': ['trope', 'tropes', 'sterotype', 'miscommunication'],
    'action':['action','intense','murder','villain','suspense', 'suspenseful']}

for new_column, word_list in feature_dict.items():
    get_feature(kdramas,'Reviews_Clean', new_column, word_list)
    
# save updated data frame with features to csv
filepath = os.path.join(PATH,'kdramas_features')
kdramas.to_csv(filepath,index=False,encoding='utf-8')
