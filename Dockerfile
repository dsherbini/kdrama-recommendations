# Dockerfile

# Set base image in Python
FROM python:3.10-slim

# Define app name
LABEL app.name="Kdramarama"

# Set working directory
WORKDIR /kdrama-recommendations

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker's caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Download necessary NLTK and TextBlob corpora
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); \
    nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); \
    nltk.download('vader_lexicon'); nltk.download('omw-1.4'); nltk.download('punkt_tab')"

RUN python -c "import textblob.download_corpora; textblob.download_corpora.download_all()"

# Create a persistent directory for data
RUN mkdir -p /kdrama-recommendations/data

# Copy the rest of the application code into the container
COPY . .

# Expose the Streamlit port
EXPOSE 8502

# Add a healthcheck for the container
HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health

# Run all commands sequentially in one line: generate drama data as csv, then run app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8502", "--server.address=0.0.0.0"]

