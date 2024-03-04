FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim-2024-03-04

## Install python-ags4
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN rm -rf /app/*
COPY ./app /app/app
