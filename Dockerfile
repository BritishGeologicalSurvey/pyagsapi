FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim-2023-02-20

## Install python-ags4
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN rm -rf /app/*
COPY ./app /app/app
