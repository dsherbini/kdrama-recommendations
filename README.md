# 🌸 Kdramarama 🌸

Kdramarama is a web application for k-drama recommendations. Recommendations are based on my personal reviews of 150+ k-dramas. View the app here: [https://k-drama-rama.com](https://k-drama-rama.com)  

## Features
- Get recommendations by selecting a k-drama from a list of titles
- View details of recommended dramas including genres, ratings, and descriptions

## Tech Stack
- **Frontend:** React, TailwindCSS 
- **Backend:** FastAPI  
- **Scraper:** BeautifulSoup, requests, selenium
- **NLP:** NLTK, gensim, spacy, textblob
- **Recommendations:** scikit-learn
- **Deployment:**  
  - Backend → Heroku  
  - Frontend → Vercel
 
 ## Data
 Data on dramas (titles, images, ratings, genres, etc.) is sourced from MyDramaList. My personal watchlist and reviews are the primary text source for feature engineering (more details below).

 ## Recommendations
 I use my personal reviews of 150+ kdramas as the basis for the recommendation engine. Steps include:
 
 - **Text Cleaning & Preprocessing**: Remove punctuation, convert to lowercase, tokenize text, remove stopwords, and lemmatize words for analysis.
- **Word & Phrase Frequency Analysis**: I use CountVectorizer and TextBlob to extract common words and phrases in my drama reviews, and visualize the results with word clouds.
- **Semantic Similarity Analysis**: I then use Word2Vec embeddings to measure similarity between extracted phrases based on cosine similarity in order to consolidate similar phrases and refine a list of common themes to provide a starting point for feature engineering.
- **Sentiment Analysis**: I use NLTK's sentiment library to generate sentiment polarity scores for each review, as well as context-specific polarity scores for specific key phrases found in reviews (these phrases are gleaned in the previous step).
- **Feature Engineering**: I use review and phrase-specific polarity scores as features. Additionally, I also creates binary features based on key words and phrases found in reviews.
- **Recommendation Model**: My recommendation model computes cosine similary for all drama titles in order to generate the N most similar dramas to a selected title.

---

## Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/dsherbini/kdrama-recommendations
cd kdrama-recommendations
```

### 2. Backend Setup (FastAPI)

#### Prerequisites
- Python 3.11+

#### Install requirements
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Run the Backend
```bash
uvicorn main:app --reload
```
The API should be available at [http://localhost:8000](http://localhost:8000).

### 3. Frontend Setup (React)
```bash
cd frontend
npm install
npm start
```
The frontend will run at [http://localhost:3000](http://localhost:3000).

### 4. Linking Frontend & Backend Locally
Create a `.env` file in the `frontend/` directory:
```
REACT_APP_API_URL=http://localhost:8000
```


