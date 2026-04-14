# Machine Learning Assessment – Pico-8 Scraper + RAG

## Overview
This project extracts 100 game entries and builds a local RAG system to generate Pico-8 code.

## Features
- Robust scraping with error handling
- Extracts:
  - Name
  - Author
  - Artwork
  - Code
  - License
  - Likes
  - Description
  - Top comments
- Local vector database using FAISS
- Offline RAG system (no API required)

## Run

pip install -r requirements.txt

python scraper.py  
python rag.py  

## Output
- games_dataset.csv  
- Query-based Pico-8 code generation  

## Tech
Python, BeautifulSoup, FAISS, SentenceTransformers

## Bonus
- Handles missing data safely
- Avoids blocking using delays
- Optimized for performance