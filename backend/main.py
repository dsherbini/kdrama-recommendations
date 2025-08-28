"""
main.py
@author: dsherbini
Date: August 2025

FAST API for routing requests to the recommendation system
"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.recommendation_system import recommend_kdrama
import pandas as pd
import os

app = FastAPI()

# Enable CORS for local dev and Heroku frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", # Local dev
        "https://kdrama-recommendations-seven.vercel.app" # Vercel frontend url
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
current_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory where main.py is located
csv_path = os.path.join(current_dir, "utils", "data", "kdrama_data_with_features_2025-08-27.csv")
df = pd.read_csv(csv_path)

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

@app.get("/")
def read_root():
    return {"message": "K-Drama Recommendation API is running!", "endpoints": ["/titles", "/recommendations"]}

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
