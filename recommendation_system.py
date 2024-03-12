"""
Title: K-Drama Recommendation System
@author: dsherbini
Date: March 2023
"""

# basic packages
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# machine learning packages


# set wd
PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'

# import k-drama data
kdramas = pd.read_csv(os.path.join(PATH, 'kdramas_features'))



import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score


kdramas = kdramas.drop(['Review','Reviews_Clean'],axis = 1)
cont = kdramas.iloc[:,1:19]
bina = kdramas.iloc[:,20:]

def recommend_kdrama(selected_item, item_features, n_recommendations=5):
    '''
    Recommend kdramas to a user based on the selection of kdrama they have liked/watched. 
    Measures similarity between kdramas using cosine similarity for continuous features
    and Jaccard similarity for binary features.
    
    Parameters:
    selected_item: Title of the k-drama selected by the user
    item_features: A matrix where each row represents an kdrama (item) and each column represents a feature.
    n_recommendations: The number of recommendations to make.
    
    Returns:
    --------
    A list of recommended k-drama titles
    '''
    # separate features into binary and continuous
    continuous = ['']
    continuous_features = item_features.iloc[:,1:19]
    binary_features = item_features[:, num_continuous_features:]
    
    # Compute cosine similarity for continuous features
    cosine_sim = cosine_similarity(continuous_features)
    
    # Compute Jaccard similarity for binary features
    # Note: This is a simplified example. You might need to adapt this for your specific binary data structure.
    jaccard_sim = jaccard_score(binary_features, binary_features, average=None)
    
    # Combine the two similarity measures (e.g., by averaging)
    combined_sim = (cosine_sim + jaccard_sim) / 2
    
    # Get the top N most similar items
    top_similar_items = np.argsort(combined_sim[user_id], axis=0)[-num_recommendations:]
    
    return top_similar_items

