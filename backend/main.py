"""
main.py
@author: dsherbini
Date: August 2025

FAST API for routing requests to the recommendation system
"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .utils.recommendation_system import recommend_kdrama
import pandas as pd

app = FastAPI()

# List all allowed origins
#origins = [
#    "http://localhost:3000",  # Local dev
#    "https://kdramarama-staging-d400cc47efde.herokuapp.com",  # Staging frontend
#    "https://kdramarama-production-169470a72f48.herokuapp.com",  # Production frontend
#]

# Enable CORS for local dev and Heroku frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kdramarama-staging-d400cc47efde.herokuapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
df = pd.read_csv("utils/data/kdrama_data_with_features_2025-08-27.csv")

# Process features for recommendation system
def process_features(df):
    cols_to_drop = ['Review','Link','Image','Score','Synopsis','Reviews_Clean', 'Korean Title', 'Translated Title','Year','Rating','Genres']
    df = df.drop(cols_to_drop, axis=1)
    df = df.apply(lambda row: row.fillna(row['Polarity_Score']), axis=1)
    features = df.copy()
    features.set_index('Title', inplace=True)
    return features

features = process_features(df)

# API model
class RecommendRequest(BaseModel):
    title: str
    n: int

@app.get("/titles")
def get_titles():
    return df['Title'].unique().tolist()

@app.post("/recommendations")
def get_recommendations(req: RecommendRequest):
    recs = recommend_kdrama(req.title, features, n=req.n)
    results = []
    for r in recs:
        rec_data = df[df['Title'] == r].iloc[0]
        results.append({
            "title": r,
            "korean_title": rec_data.get('Korean Title'),
            "translated_title": rec_data.get('Translated Title'),
            "link": rec_data.get('Link'),
            "image": rec_data.get('Image'),
            "rating": rec_data.get('Rating'),
            "synopsis": rec_data.get('Synopsis'),
            "genres": rec_data.get('Genres')
        })
    return results
