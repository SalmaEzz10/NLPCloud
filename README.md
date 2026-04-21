# Arabic NER API

This project provides a RESTful API built with **FastAPI** to analyze Egyptian addresses and extract their components such as street, area, city, building, apartment, floor, and landmark.

## Project Structure
- `main.py` : Entry point of the FastAPI application.
- `preprocess.py` : Preprocessing utilities for text normalization.
- `ner_model/` : Trained Named Entity Recognition model and related files.
- `requirements.txt` : Python dependencies.
- `Dockerfile` : Instructions to build the Docker image.

## Run Locally
Clone the repository and install dependencies:
```bash
git clone this repo
cd arabic-ner-api
pip install -r requirements.txt
uvicorn main:app --reload
