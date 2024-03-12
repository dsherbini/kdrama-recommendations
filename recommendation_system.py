"""
Title: K-Drama Recommendation System
@author: dsherbini
Date: March 2023
"""

# load packages
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score

# set wd
PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

# import k-drama data
kdramas = pd.read_csv(os.path.join(PATH, 'kdramas_features'))

################################ DATA CLEANING ################################

# drop review columns from the df
kdramas = kdramas.drop(['Review','Reviews_Clean'],axis = 1)

# fill NaNs with the general polarity scores for all continuous feature columns
kdramas = kdramas.apply(lambda row: row.fillna(row['Polarity_Score']), axis=1)

# split into continuous and binary features
continuous_features = kdramas.iloc[:,1:19]
binary_features = kdramas.iloc[:,20:]


############################### RECOMMENDATIONS ###############################


def recommend_kdrama(selected_title, continuous_features, binary_features, n_recommendations=5):
    '''
    Recommend kdramas to a user based on the selection of kdrama they have liked/watched. 
    Measures similarity between kdramas using cosine similarity for continuous features
    and Jaccard similarity for binary features.
    
    Parameters:
    selected_title: Title of the k-drama selected by the user
    continuous_features: a df/matrix of continuous features where each column represents a kdrama
    binary_features: a df/matrix of binary features where each column represents a kdrama
    n_recommendations: The number of recommendations to make (default is 5)
    
    Returns:
    --------
    A list of recommended k-drama titles
    '''
    
    # compute cosine similarity for continuous features
    cosine_sim = cosine_similarity(continuous_features)
    
    # compute Jaccard similarity for binary features
    jaccard_sim = jaccard_score(binary_features, binary_features, average=None)
    
    # take the average of the two similarity scores
    combined_sim = (cosine_sim + jaccard_sim) / 2
    
    # get the top N most similar items
    top_similar_items = np.argsort(combined_sim[selected_title], axis=0)[-n_recommendations:]
    
    return top_similar_items

cosine_sim = cosine_similarity(continuous_features)
    
    # compute Jaccard similarity for binary features
jaccard_sim = jaccard_score(binary_features, binary_features, average=None)
    
    # take the average of the two similarity scores
combined_sim = (cosine_sim + jaccard_sim) / 2
    
    # get the top N most similar items
top_similar_items = np.argsort(combined_sim[selected_title], axis=0)[-n_recommendations:]