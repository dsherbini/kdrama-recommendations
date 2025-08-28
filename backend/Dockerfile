FROM python:3.10-slim

LABEL app.name="Kdramarama-Backend"

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend code
COPY . .

# Expose Heroku port
ENV PORT 8080
EXPOSE $PORT

# Run FastAPI backend -- development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

# Run FastAPI backend -- production
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
