"""
Title: K-Drama Recommendation System
@author: dsherbini
Date: March 2023
"""

# load packages
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# set wd
PATH = '/Users/danya/Documents/GitHub/personal github/kdrama-recommendations'
os.chdir(PATH)

# load data
kdramas = pd.read_csv('data/kdrama_data_with_features.csv')

################################ DATA CLEANING ################################

# drop review columns from the df
kdramas = kdramas.drop(['Review','Reviews_Clean'],axis = 1)

# fill NaNs with the general polarity scores for all continuous feature columns
kdramas = kdramas.apply(lambda row: row.fillna(row['Polarity_Score']), axis=1)

# for features df, set index as title
features = kdramas.copy()
features.set_index('Title', inplace=True)


############################### RECOMMENDATIONS ###############################

def recommend_kdrama(selected_title, features, n=5):
    '''
    Recommend kdramas to a user based on the selection of kdrama they have liked/watched. 
    Measures similarity between kdramas using cosine similarity.
    
    Parameters:
    selected_title: Title of the k-drama selected by the user
    features: A dataframe of features for each k-drama (with Title as the index)
    n: The number of recommendations to make (default is 5)
    
    Returns:
    --------
    A list of recommended k-drama titles
    '''
    
    # select the features of the selected k-drama
    selected_kdrama_features = features.loc[selected_title]
    
    # convert the selected row to a numpy array and reshape it
    selected_kdrama_features_array = np.array(selected_kdrama_features).reshape(1, -1)
    
    # calculate cosine similarity between the selected k-drama and all others
    similarity_scores = cosine_similarity(selected_kdrama_features_array, features)
    
    # set number of recommendations as inputted n value +1 
    # (because similarity scores will include the selected title itself)
    n_recommendations = n+1
    
    # get the indices of the top N most similar k-dramas
    top_indices = np.argsort(similarity_scores[0])[-n_recommendations:][::-1]

    # get the titles of the most similar k-dramas
    recommended_kdramas = features.iloc[top_indices].index
    
    # remove the selected title from the list of final recommendations
    recommendations = [row for row in recommended_kdramas if row != selected_title]
    
    return recommendations


